import sqlite3
from datetime import datetime
from pathlib import Path
from uuid import uuid4
import urllib.parse

from .passwords import hash_password, verify_password


class DBObject:
    """
    This is an abstract class used for communicating with a SQLite database.
    It should be subclassed in order to make data models that can be retrieved
    from and saved to a database.

    The default behaviors for this class assume you will have an autoincremented
    column called `id` for your primary key. If that is not the case, you
    will have to override some behavior.
    """
    table_name = None

    @classmethod
    def create_table(cls, db, recreate=False):
        """
        Create a table for the DBObject.
        """
        if recreate:
            cls.drop_table(db)
        with db:
            db.execute(cls.create_table_sql())

    @classmethod
    def drop_table(cls, db):
        """
        Drop the table for the DBObject.
        """
        with db:
            db.execute(f"DROP TABLE {cls.table_name}")

    @classmethod
    def select(cls, db, sql_fragment="", params=None):
        """
        Run a SELECT statement and return the results as
        DBObjects. The inheriting DBObject class should implement
        an __init__ method that can take all database fields as
        arguments.
        """
        if params is None:
            params = []
        sql, params = cls.select_sql(sql_fragment, params)
        with db:
            db.row_factory = sqlite3.Row
            cursor = db.execute(sql, params)
            return [cls(**row) for row in cursor.fetchall()]

    @classmethod
    def create_table_sql(cls):
        """
        Implement this in order to generate the CREATE TABLE statement
        needed to make your database table.
        """
        raise NotImplementedError

    @classmethod
    def select_sql(cls, sql_fragment, params):
        """
        Override this in order to generate the SELECT statement
        needed to get back data from your database.
        """
        sql = f"SELECT * FROM {cls.table_name} {sql_fragment}"
        return sql, params

    def __init__(self, **kwargs):
        """
        By default, we take all keyword arguments and assign those
        to attributes on the DBObject. This should be overridden
        if you want behavior different than that.
        """
        self.id = None
        self.errors = []
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self, db):
        """
        Given a database object, save it to the database. This will run
        several "hooks" on the object:

        - validate() -- if this fails, stop
        - before_save()
        - save_sql() -- returns sql + parameters
        - after_save()
        """
        if self.validate(db):
            self.before_save(db)
            sql, params = self.save_sql()
            with db:
                cursor = db.execute(sql, params)
                if self.id is None:
                    self.id = cursor.lastrowid
            self.after_save(db)
            return True
        return False

    def save_sql(self):
        """
        Implement this in order to generate the SQL you need to
        save your record to your database. This should return a
        tuple, with the first element being SQL and the second
        being a list of parameters.
        """
        raise NotImplementedError

    def delete(self, db):
        """
        Given a database object, remove it from the database. This
        will run several "hooks" on the object:

        - before_delete()
        - delete_sql() -- returns sql + parameters
        - after_delete()
        """

        if self.id:
            self.before_delete(db)
            sql, params = self.delete_sql(db)
            with db:
                db.execute(sql, params)
            self.after_save(db)

    def delete_sql(self, db=None):
        """
        Override this in order to generate the SQL you need to
        delete your record from your database. This should return a
        tuple, with the first element being SQL and the second
        being a list of parameters.
        """
        if not self.id:
            return False
        sql = f"DELETE FROM {self.table_name} WHERE id = ?"
        return sql, [self.id]

    def to_dict(self):
        """
        Implement this so your DBObject can be turned into a dictionary.
        This will be needed in our API.
        """
        raise NotImplementedError

    def validate(self, db=None):
        """
        Override this to check your object for any errors before
        saving to the database. It should return a boolean,
        True if valid, False if not. It can populate the `self.errors`
        list.
        """
        return True

    def before_save(self, db=None):
        """
        Override this for any before-save actions.
        """
        pass

    def after_save(self, db=None):
        """
        Override this for any after-save actions.
        """
        pass

    def before_delete(self, db=None):
        """
        Override this for any before-delete actions.
        """
        pass

    def after_delete(self, db=None):
        """
        Override this for any after-delete actions.
        """
        pass


class Page(DBObject):
    """
    A Page is one individual page in our wiki.
    The content of the page is held in the page history.
    """

    table_name = "pages"

    @classmethod
    def create_table_sql(cls):
        return """
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE
        )
        """

    @classmethod
    def create_with_body(cls, db, title, body, user_id=None):
        page = cls(title=title)
        if page.validate(db) and body:
            page.save(db)
            version = PageVersion(body=body, page_id=page.id, user_id=user_id)
            version.save(db)
        elif not body:
            page.errors.append(["body", "page must contain a body"])

        return page

    @classmethod
    def get_by_title(cls, db, title):
        pages = cls.select(db, "WHERE title = ?", [title])
        if pages:
            return pages[0]

    def __init__(self, id=None, title=None, history=None):
        super().__init__()
        self.id = id
        self.title = title
        self.history = None

    def save_sql(self):
        if self.id:
            return "UPDATE pages SET title = ? WHERE id = ?", [
                self.title, self.id
            ]

        return "INSERT INTO pages (title) VALUES (?)", [self.title]

    def validate(self, db):
        self.errors = []
        if not self.title:
            self.errors.append(["title", "title is required"])
            return False

        if self.id:
            title_matches = self.select(db, "WHERE title = ? AND id != ?",
                                        [self.title, self.id])
        else:
            title_matches = self.select(db, "WHERE title = ?", [self.title])

        if title_matches:
            self.errors.append(["title", "title must be unique"])
            return False

        return True

    def with_history(self, db):
        self.history = PageVersion.select(
            db, "WHERE page_id = ? ORDER BY saved_at DESC", [self.id])
        return self

    def add_version(self, db, body, user_id=None):
        version = PageVersion(body=body, page_id=self.id, user_id=user_id)
        version.save(db)
        if self.history:
            self.history.insert(0, version)
        return version

    def before_delete(self, db):
        sql = f"DELETE FROM {PageVersion.table_name} WHERE page_id = ?"
        with db:
            db.execute(sql, [self.id])

    def to_dict(self, all_history=False):
        retval = {
            "id": self.id,
            "title": self.title,
            "url": f"/pages/{urllib.parse.quote(self.title)}/"
        }
        if self.history:
            retval['body'] = self.history[0].body
            retval['updated_at'] = self.history[0].saved_at
            retval['updated_by'] = self.history[0].user_id
            if all_history:
                retval['history'] = [{
                    "body": version.body,
                    "saved_at": version.saved_at,
                    "user_id": version.user_id
                } for version in self.history]
        return retval


class PageVersion(DBObject):
    table_name = 'page_versions'

    @classmethod
    def create_table_sql(cls):
        return """
        CREATE TABLE IF NOT EXISTS page_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_id INTEGER REFERENCES pages(id),
            body TEXT,
            user_id INTEGER REFERENCES users(id) NULL,
            saved_at TIMESTAMP
        )
        """

    def __init__(self,
                 page_id=None,
                 id=None,
                 body=None,
                 user_id=None,
                 saved_at=None):
        super().__init__()
        self.id = id
        self.page_id = page_id
        self.body = body
        self.saved_at = saved_at
        self.user_id = user_id

    def save_sql(self):
        if self.id:
            return "UPDATE page_versions SET page_id = ?, body = ?, saved_at = ?, user_id = ? WHERE id = ?", [
                self.page_id, self.body, self.saved_at, self.user_id, self.id
            ]

        return "INSERT INTO page_versions (page_id, body, user_id, saved_at) VALUES (?, ?, ?, ?)", [
            self.page_id, self.body, self.user_id, self.saved_at
        ]

    def before_save(self, db=None):
        self.saved_at = datetime.now()

    def validate(self, db=None):
        if not (self.body and self.page_id):
            return False
        return True


class User(DBObject):
    table_name = "users"

    @classmethod
    def create_table_sql(cls):
        return """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            encrypted_password TEXT,
            token TEXT
        )
        """

    @classmethod
    def get_by_username(cls, db, username):
        users = cls.select(db, "WHERE username = ?", [username])
        if users:
            return users[0]

    @classmethod
    def get_by_token(cls, db, token):
        users = cls.select(db, "WHERE token = ?", [token])
        if users:
            return users[0]

    def __init__(self,
                 id=None,
                 username=None,
                 password=None,
                 encrypted_password=None,
                 token=None):
        super().__init__()
        self.id = id
        self.username = username
        self.encrypted_password = encrypted_password
        self.password = password
        self.token = token

    def password_matches(self, password):
        if not self.encrypted_password:
            return False
        return verify_password(self.encrypted_password, password)

    def before_save(self, db=None):
        if self.password:
            self.encrypted_password = hash_password(self.password)
        self.set_token()

    def set_token(self):
        if not self.token:
            self.token = str(uuid4())

    def save_sql(self):
        if self.id:
            return "UPDATE users SET username = ?, encrypted_password = ?, token = ? WHERE id = ?", [
                self.username, self.encrypted_password, self.token, self.id
            ]

        return "INSERT INTO users (username, encrypted_password, token) VALUES (?, ?, ?)", [
            self.username, self.encrypted_password, self.token
        ]

    def validate(self, db):
        self.errors = []

        if not self.username:
            self.errors.append(['username', 'username is required'])
            return False

        if self.id:
            username_matches = self.select(db, "WHERE username = ? AND id != ?",
                                           [self.username, self.id])
        else:
            username_matches = self.select(db, "WHERE username = ?",
                                           [self.username])

        if username_matches:
            self.errors.append(['username', 'username must be unique'])
            return False

        if not self.password and not self.encrypted_password:
            self.errors.append(['password', 'password is required'])
            return False

        return True

    def to_dict(self):
        return {"username": self.username}


def load_pages(db_path):
    db = sqlite3.connect(db_path)
    PageVersion.create_table(db, recreate=True)
    Page.create_table(db, recreate=True)

    pages_dir = Path(__file__).parent / '..' / 'pages'
    pages = pages_dir.glob("*.md")
    for page_path in pages:
        with open(page_path, 'r') as file:
            title = file.readline().strip()
            body = file.read().strip()
            print(title)
            page = Page(title=title)
            page.save(db)
            version = PageVersion(body=body, page_id=page.id)
            version.save(db)

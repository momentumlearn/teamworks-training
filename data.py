import sqlite3
from datetime import datetime
from pathlib import Path


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
    table_name = "pages"

    @classmethod
    def create_table_sql(cls):
        return """
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            body TEXT,
            title TEXT UNIQUE,
            updated_at DATETIME
        )
        """

    def __init__(self, id=None, title=None, body=None, updated_at=None):
        super().__init__()
        self.id = id
        self.title = title
        self.body = body
        self.updated_at = updated_at

    def save_sql(self):
        if self.id:
            sql = "UPDATE pages SET title = ?, body = ? WHERE id = ?"
            return (sql, [self.title, self.body, self.id])
        sql = "INSERT INTO PAGES (title, body) VALUES (?, ?)"
        return (sql, [self.title, self.body])

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "updated_at": self.updated_at
        }

    def validate(self, db=None):
        self.errors = []
        if not self.title:
            self.errors.append(["title", "is required"])
            return False

        if not self.body:
            self.errors.append(["body", "is required"])
            return False

        if self.id:
            title_matches = self.select(db, "WHERE title = ? AND id != ?",
                                        [self.title, self.id])
        else:
            title_matches = self.select(db, "WHERE title = ?", [self.title])

        if title_matches:
            self.errors.append(["title", "must be unique"])
            return False

        return True

    def before_save(self, db=None):
        self.updated_at = datetime.now()


# Exercise: create a User class. Users should have a username and password.
# Passwords shouldn't be in cleartext, but try that first. If you get through that,
# change it to have an encrypted password.
# Before save, if there’s a password field set, encrypt the password using the
# function hash_password from passwords.py.


def load_pages(db_path):
    db = sqlite3.connect(db_path)
    Page.create_table(db)

    pages_dir = Path(__file__).parent / 'pages'
    pages = pages_dir.glob("*.md")
    for page_path in pages:
        with open(page_path, 'r') as file:
            title = file.readline().strip()
            body = file.read().strip()
            print(title)
            page = Page(title=title, body=body)
            page.save(db)

import sqlite3
from datetime import datetime


class Database:
    """
    This class controls access to a database. Unlike some
    ORMs, we use a database object and pass our DBObjects to it in order
    to save to a database and retrieve information from it.
    """

    def __init__(self, dbfile):
        """
        Establish a connection to the database. We set the
        row_factory in order to get back dict-like objects from 
        the database.
        """
        self.con = sqlite3.connect(dbfile)
        self.con.row_factory = sqlite3.Row

    def create_table(self, dbobj_class, recreate=False):
        """
        Create a table for the DBObject. The DBObject should
        handle making the DDL, but this method will generate
        a DROP TABLE statement if `recreate` is True.
        """
        if recreate:
            self.drop_table(dbobj_class)
        with self.con:
            self.con.execute(dbobj_class.create_table_sql())

    def drop_table(self, dbobj_class):
        """
        Drop the table for the DBObject.
        """
        with self.con:
            self.con.execute(f"DROP TABLE {dbobj_class.table_name}")

    def select(self, dbobj_class, sql_fragment="", params=None):
        """
        Run a SELECT statement and return the results as
        DBObjects. The inheriting DBObject class should implement
        an __init__ method that can take all database fields as
        arguments.
        """
        if params is None:
            params = []
        sql, params = dbobj_class.select_sql(sql_fragment, params)
        with self.con:
            cursor = self.con.execute(sql, params)
            return [dbobj_class(**row) for row in cursor.fetchall()]

    def save(self, dbobj):
        """
        Given a database object, save it to the database. This will run
        several "hooks" on the object:

        - validate() -- if this fails, stop
        - before_save()
        - save_sql() -- returns sql + parameters
        - after_save()
        """
        if dbobj.validate():
            dbobj.before_save()
            sql, params = dbobj.save_sql()
            with self.con:
                cursor = self.con.execute(sql, params)
                if dbobj.id is None:
                    dbobj.id = cursor.lastrowid
            dbobj.after_save()
            return True
        return False

    def delete(self, dbobj):
        """
        Given a database object, remove it from the database. This
        will run several "hooks" on the object:

        - before_delete()
        - delete_sql() -- returns sql + parameters
        - after_delete()
        """

        if dbobj.id:
            dbobj.before_delete()
            sql, params = dbobj.delete_sql()
            with self.con:
                self.con.execute(sql, params)
            dbobj.after_save()


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

    def save_sql(self):
        """
        Implement this in order to generate the SQL you need to
        save your record to your database. This should return a
        tuple, with the first element being SQL and the second
        being a list of parameters.
        """
        raise NotImplementedError

    def delete_sql(self):
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

    def validate(self):
        """
        Override this to check your object for any errors before
        saving to the database. It should return a boolean,
        True if valid, False if not. It can populate the `self.errors`
        list.
        """
        return True

    def before_save(self):
        """
        Override this for any before-save actions.
        """
        pass

    def after_save(self):
        """
        Override this for any after-save actions.
        """
        pass

    def before_delete(self):
        """
        Override this for any before-delete actions.
        """
        pass

    def after_delete(self):
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
        CREATE TABLE pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE
        )
        """

    def __init__(self, id=None, title=None, history=None):
        super().__init__()
        self.id = id
        self.title = title
        self.history = history or []

    def save_sql(self):
        if self.id:
            return "UPDATE pages SET title = ? WHERE id = ?", [
                self.title, self.id
            ]

        return "INSERT INTO pages (title) VALUES (?)", [self.title]

    def validate(self):
        if not self.title:
            return False
        return True


class PageVersion(DBObject):
    table_name = 'page_versions'

    @classmethod
    def create_table_sql(cls):
        return """
        CREATE TABLE page_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_id INTEGER REFERENCES pages(id),
            body TEXT,
            saved_at TIMESTAMP            
        )
        """

    @classmethod
    def select_sql(cls, sql_fragment, params):
        """
        Override this in order to generate the SELECT statement
        needed to get back data from your database.
        """
        sql, params = super().select_sql(sql_fragment, params)
        if "ORDER BY" not in sql.upper():
            sql_parts = sql.split(" ")
            idx = 0
            for idx, part in enumerate(sql_parts):
                if part.upper() == "LIMIT" or part.upper() == "OFFSET":
                    break

            sql_parts.insert(idx, "ORDER BY saved_at")
            sql = " ".join(sql_parts)

        return sql, params

    def __init__(self, page_id=None, id=None, body=None, saved_at=None):
        super().__init__()
        self.id = id
        self.page_id = page_id
        self.body = body
        self.saved_at = saved_at

    def save_sql(self):
        if self.id:
            return "UPDATE page_versions SET page_id = ?, body = ?, saved_at = ? WHERE id = ?", [
                self.page_id, self.body, self.saved_at, self.id
            ]

        return "INSERT INTO page_versions (page_id, body, saved_at) VALUES (?, ?, ?)", [
            self.page_id, self.body, self.saved_at
        ]

    def before_save(self):
        self.saved_at = datetime.now()

    def validate(self):
        if not self.body:
            return False
        return True

import sqlite3


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

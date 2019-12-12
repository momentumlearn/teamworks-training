import sqlite3

import click
from flask import current_app, g
from .data import Page, PageVersion, User


def get_db():
    """
    Establish a per-thread connection to the database.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(str(current_app.config['DATABASE']))
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Make sure our database tables are created.
    """
    db = get_db()
    Page.create_table(db)
    PageVersion.create_table(db)
    User.create_table(db)


def init_app(app):
    """
    Create our database tables and ensure the DB connection is closed
    when the app ends.
    """
    app.teardown_appcontext(close_db)
    init_db()

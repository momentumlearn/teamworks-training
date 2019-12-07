import sqlite3
from data import DBObject, Page, PageVersion
from flask import Flask, g
app = Flask(__name__)

DATABASE = 'wiki.sqlite3'


def get_db():
    """
    Establish a per-thread connection to the database.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


with app.app_context():
    db = get_db()
    Page.create_table(db)
    PageVersion.create_table(db)


@app.route("/pages/")
def pages_list():
    pages = Page.select(get_db())
    return {"pages": [page.to_dict() for page in pages]}

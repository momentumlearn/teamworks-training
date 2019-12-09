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
def page_list():
    pages = [page.to_dict() for page in Page.select(get_db())]
    for page in pages:
        last_version = PageVersion.select(
            get_db(), "WHERE page_id = ? ORDER BY saved_at DESC LIMIT 1",
            [page['id']])
        if last_version[0]:
            page['body'] = last_version[0].body
            page['last_updated_at'] = last_version[0].saved_at
    return {"pages": pages}


@app.route("/pages/<title>")
def page_detail(title):
    page = Page.select(get_db(), "WHERE title = ?", [title])[0]
    if page:
        page = page.to_dict()
        last_version = PageVersion.select(
            get_db(), "WHERE page_id = ? ORDER BY saved_at DESC LIMIT 1",
            [page['id']])
        if last_version[0]:
            page['body'] = last_version[0].body
            page['last_updated_at'] = last_version[0].saved_at
        return page
    else:
        return '', 404

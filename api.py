import sqlite3
from data import DBObject, Page, PageVersion
from flask import Flask, g, request
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


@app.route("/pages/", methods=['GET', 'POST'])
def page_list():
    db = get_db()

    if request.method == 'POST':
        return create_page(request)
    else:
        return {
            "pages": [
                page.with_history(db).to_dict() for page in Page.select(db)
            ]
        }


@app.route("/pages/<title>/")
def page_detail(title):
    db = get_db()
    page = Page.select(db, "WHERE title = ?", [title])[0]
    if page:
        return page.with_history(db).to_dict()
    else:
        return '', 404


def create_page(request):
    data = request.get_json()
    page = Page.create_with_body(
        db, title=data.get('title'), body=data.get('body'))
    if page.errors:
        return ({"errors": page.errors}, 422)
    else:
        return page.with_history(db).to_dict(), 201

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


@app.route("/pages/<title>/", methods=['GET', 'PUT', 'DELETE'])
def page_detail(title):
    db = get_db()
    page = Page.get_by_title(db, title)
    if page:
        if request.method == "PUT":
            return update_page(request, page)
        elif request.method == "DELETE":
            return delete_page(request, page)
        else:
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


def update_page(request, page):
    data = request.get_json()
    if data.get('title'):
        page.title = data.get('title')
        page.save(get_db())
    if data.get('body'):
        page.add_version(get_db(), data.get('body'))

    return page.with_history(get_db()).to_dict()


def delete_page(request, page):
    page.delete(get_db())
    return "", 204

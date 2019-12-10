from flask import Flask, request, g
import sqlite3
from data import Page, User

app = Flask(__name__)
DATABASE = 'wiki.sqlite3'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


with app.app_context():
    db = get_db()
    Page.create_table(db)
    User.create_table(db)


@app.before_request
def load_user():
    if request.headers.get('Authorization') and request.headers[
            'Authorization'].startswith("Token"):
        _, token = request.headers.get('Authorization').split(" ")
        user = User.get_by_token(get_db(), token)
        g.user = user
    else:
        g.user = None


@app.route("/pages/", methods=['GET', 'POST'])
def page_list():
    if request.method == "POST":
        return create_page()

    db = get_db()
    pages = Page.select(db)

    return {"pages": [page.to_dict() for page in pages]}


def create_page():
    if not g.user:
        return "", 401

    db = get_db()

    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    page = Page(title=title, body=body, updated_by=g.user.id)

    if page.validate(db):
        page.save(db)
        return page.to_dict(), 201
    else:
        return ({"errors": page.errors}, 422)

    return data


@app.route("/pages/<title>/", methods=["GET", "PUT", "DELETE"])
def page_detail(title):
    db = get_db()
    pages = Page.select(db, "WHERE title = ?", [title])
    if pages:
        page = pages[0]

        if request.method == "PUT":
            return update_page(page)
        if request.method == "DELETE":
            if not g.user:
                return "", 401

            page.delete(db)
            return "", 204

        return page.to_dict()
    else:
        return "", 404


def update_page(page):
    if not g.user:
        return "", 401

    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    page.title = title
    page.body = body
    page.updated_by = g.user.id

    db = get_db()
    if page.validate(db):
        page.save(db)
        return page.to_dict()
    else:
        return {"errors": page.errors}, 422


@app.route("/user/", methods=["POST"])
def create_user():
    db = get_db()
    data = request.get_json()
    user = User(username=data.get('username'))
    if not data.get('password'):
        return {"errors": ["password", "is required"]}, 422
    user.set_password(data.get('password'))
    if user.validate(db):
        user.save(db)
        return user.to_dict(), 201
    else:
        return {"errors": user.errors}, 422

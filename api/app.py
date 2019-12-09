import sqlite3
from pathlib import Path

from flask import Flask, g, request, current_app

from .data import DBObject, Page, PageVersion
from .db import init_app as db_init_app, get_db


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', DATABASE=Path(__file__).parent / 'wiki.sqlite3')

    with app.app_context():
        db_init_app(app)

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

    return app


def create_page(request):
    data = request.get_json()
    db = get_db()
    page = Page.create_with_body(
        db, title=data.get('title'), body=data.get('body'))
    if page.errors:
        return ({"errors": page.errors}, 422)
    else:
        return page.with_history(db).to_dict(), 201


def update_page(request, page):
    data = request.get_json()
    db = get_db()
    if data.get('title'):
        page.title = data.get('title')
        page.save(db)
    if data.get('body'):
        page.add_version(db, data.get('body'))

    return page.with_history(db).to_dict()


def delete_page(request, page):
    page.delete(get_db())
    return "", 204

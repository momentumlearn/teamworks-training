import sqlite3
from pathlib import Path

from flask import Flask, g, request, current_app

from .data import DBObject, Page, PageVersion


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', DATABASE=Path(__file__).parent / 'wiki.sqlite3')

    with app.app_context():
        from . import db
        db.init_app(app)

    from . import pages, auth
    app.register_blueprint(pages.bp)
    app.register_blueprint(auth.bp)

    return app

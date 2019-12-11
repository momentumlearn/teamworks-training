from flask import Blueprint, request, g

from .data import Page
from .db import get_db
from .auth import login_required

bp = Blueprint('pages', __name__, url_prefix='/pages')


@bp.route("/", methods=['GET', 'POST'])
def page_list():
    db = get_db()

    if request.method == 'POST':
        return create_page()
    else:
        return {
            "pages": [
                page.with_history(db).to_dict() for page in Page.select(db)
            ]
        }


@bp.route("/<title>/", methods=['GET', 'PUT', 'DELETE'])
def page_detail(title):
    db = get_db()
    page = Page.get_by_title(db, title)
    if page:
        if request.method == "PUT":
            return update_page(page)
        elif request.method == "DELETE":
            return delete_page(page)
        else:
            return page.with_history(db).to_dict()
    else:
        return '', 404


@login_required
def create_page():
    data = request.get_json()
    db = get_db()
    page = Page.create_with_body(
        db, title=data.get('title'), body=data.get('body'))
    if page.errors:
        return ({"errors": page.errors}, 422)
    else:
        return page.with_history(db).to_dict(), 201


@login_required
def update_page(page):
    data = request.get_json()
    db = get_db()
    if data.get('title'):
        page.title = data.get('title')
        page.save(db)
    if data.get('body'):
        page.add_version(db, data.get('body'), user_id=g.user.id)

    return page.with_history(db).to_dict()


@login_required
def delete_page(page):
    page.delete(get_db())
    return "", 204

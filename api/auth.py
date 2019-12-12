from functools import wraps
from flask import Blueprint, g, request

from .data import User
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return "", 401
        return f(*args, **kwargs)

    return decorated_function


@bp.before_app_request
def load_user():
    if request.headers.get('Authorization') and request.headers[
            'Authorization'].startswith("Token"):
        _, token = request.headers.get('Authorization').split(" ")
        user = User.get_by_token(get_db(), token)
        g.user = user
    else:
        g.user = None


@bp.route('/user/', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        return register_user()
    else:
        return show_user()


@login_required
def show_user():
    return g.user.to_dict()


def register_user():
    db = get_db()
    data = request.get_json()
    user = User(username=data.get('username'), password=data.get('password'))
    if user.validate(db):
        user.save(db)
        return {"username": user.username, "token": user.token}, 201
    return {"errors": user.errors}, 422


@bp.route('/token/', methods=['POST'])
def get_token():
    db = get_db()
    data = request.get_json()
    username, password = (data.get('username'), data.get('password'))
    user = User.get_by_username(db, username)
    if not user or not user.password_matches(password):
        return {"errors": ["no user with that username and password"]}
    if not user.token:
        user.set_token()
        user.save(db)
    return {"token": user.token}

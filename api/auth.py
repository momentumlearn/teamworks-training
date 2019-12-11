from flask import Blueprint, g, request

from .data import User
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/user/', methods=['POST'])
def register_user():
    db = get_db()
    data = request.get_json()
    user = User(username=data.get('username'), password=data.get('password'))
    if user.validate(db):
        user.save(db)
        return {"username": user.username}, 201
    return {"errors": user.errors}, 422

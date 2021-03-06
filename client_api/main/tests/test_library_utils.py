# import unittest
from .. import db, create_app
from flask import current_app
# def test_metatags():
#     pass

def test_encode_decode_auth():
    from ..library import encode_auth_token, decode_auth_token
    from ..users.models import UserModel
    if not current_app:
        app = create_app()
        app.app_context().push()
    else:
        app = current_app

    with app.app_context():
        users_list = UserModel.query.filter_by().all()
        if isinstance(users_list, list) and len(users_list) > 0:
            user_instance = users_list[0]

            token = encode_auth_token(user_instance.uid)
            assert user_instance.uid == decode_auth_token(token), 'Encode and Decode utils not functioning correctly'
        else:
            assert False , "Test did not run as there are no user records"


def test_authenticated_user():
    pass


def test_is_authenticated():
    pass
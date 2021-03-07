# import unittest
from .. import db, create_app
from flask import current_app
from ..library import config
# def test_metatags():
#     pass

def test_encode_decode_auth():
    from ..library import encode_auth_token, decode_auth_token
    from ..users.models import UserModel
    if not current_app:
        app = create_app(config_class=config.TestingConfig)
        app.app_context().push()
    else:
        app = current_app

    with app.app_context():
        users_list = UserModel.query.limit(1).all()
        if isinstance(users_list, list) and len(users_list) > 0:
            user_instance = users_list[0]
            token = encode_auth_token(user_instance.uid)
            assert token, "Could not encode Auth Token"
            assert decode_auth_token(token), 'Could not decode auth token'
        else:
            assert False , "Test did not run as there are no user records"


def test_authenticated_user():
    pass


def test_is_authenticated():
    pass
import datetime
import jwt
from .metatags import Metatags
from flask import current_app, jsonify, request, redirect, url_for
from functools import wraps
from ..users.models import UserModel

def encode_auth_token(uid):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,minutes=30, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': uid
        }
        return jwt.encode(
            payload=payload,
            key=current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
        return payload['sub'].decode()
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return redirect(url_for('users.login'))

        try:
            uid = decode_auth_token(auth_token=token)
            current_user = UserModel.query.filter_by(uid=uid).first()
        except Exception as error:
            return redirect(url_for('users.login'))

        return f(current_user, *args, **kwargs)
    return decorated

def is_authenticated(token):
    try:
        uid = decode_auth_token(auth_token=token)
        current_user = UserModel.query.filter_by(uid=uid).first()
        return True
    except Exception as error:
        return False

def authenticated_user(token):
    try:
        uid = decode_auth_token(auth_token=token)
        current_user = UserModel.query.filter_by(uid=uid).first()
        return current_user
    except Exception as error:
        return None

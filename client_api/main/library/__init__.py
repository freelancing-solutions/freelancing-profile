import datetime, time
import jwt
from sqlalchemy.exc import OperationalError
from .metatags import Metatags
from flask import current_app, jsonify, request, redirect, url_for, flash
from functools import wraps
from .utils import timestamp
from ..users.models import UserModel


def encode_auth_token(uid: str) -> str:
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': uid
        }
        token = jwt.encode(payload=payload, key=str(current_app.config.get('SECRET_KEY')), algorithm='HS256')
        return token.decode()
    except jwt.InvalidAlgorithmError as e:
        return str(e)


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(jwt=auth_token, key=current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError as e:
        print("Error Expired Signature")
        return None
    except jwt.InvalidTokenError as e:
        print("Error : invalid token")
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # print('token headers: {}'.format(request.headers))
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # print('token found : {}'.format(token))
        if not token:
            return redirect(url_for('users.login'))
        try:
            uid = decode_auth_token(auth_token=token)
            if uid:
                try:
                    current_user = UserModel.query.filter_by(_uid=uid).first()
                except OperationalError as e:
                    message = '''Error connecting to database or user does not exist'''
                    flash(message, 'warning')
                    current_user = None
            else:
                message: str = '''to access restricted areas of this site please login'''
                flash(message, 'warning')
                current_user = None
        except jwt.DecodeError:
            flash('Error decoding your token please login again', 'warning')
            return redirect(url_for('users.login'))
        except Exception as e:
            flash('Unable to locate your account please create a new account', 'warning')
            return redirect(url_for('users.register'))
        return f(current_user, *args, **kwargs)

    return decorated


def verify_external_auth_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        sent_data = request.get_json()
        api = sent_data['api']
        # TODO- find the api token if valid pass if not revoke
        return f(identity=api, *args, **kwargs)

    return decorated


def logged_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if token:
                try:
                    uid = decode_auth_token(auth_token=token)
                    if uid:
                        try:
                            current_user = UserModel.query.filter_by(_uid=uid).first()
                        except OperationalError as e:
                            pass
                    else:
                        pass
                except jwt.DecodeError as e:
                    # If user not logged in do nothing
                    pass
            else:
                pass
        return f(current_user, *args, **kwargs)

    return decorated


def is_authenticated(token: str) -> bool:
    try:
        uid = decode_auth_token(auth_token=token)
        current_user = UserModel.query.filter_by(_uid=uid).first()
        return True
    except jwt.DecodeError as e:
        return False


def authenticated_user(token: str):
    try:
        uid = decode_auth_token(auth_token=token)
        current_user = UserModel.query.filter_by(_uid=uid).first()
        return current_user
    except jwt.DecodeError as e:
        return None

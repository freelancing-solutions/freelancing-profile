import datetime
import jwt
from .metatags import Metatags
from flask import current_app, jsonify, request, redirect, url_for, flash
from functools import wraps
from ..users.models import UserModel


def encode_auth_token(uid):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': uid
        }
        token = jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
        return str(token)
    except jwt.InvalidAlgorithmError as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        flash('You have been logged out please login again', 'warning')
        return redirect(url_for('users.login'))
    except jwt.InvalidTokenError:
        message = '''
            You are presently not logged in, you can login to submit freelance jobs
        '''
        flash(message, 'info')
        return redirect(url_for('users.login'))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print('token headers: {}'.format(request.headers))
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # print('token found : {}'.format(token))
        if not token:
            return redirect(url_for('users.login'))
        try:
            uid = decode_auth_token(auth_token=token)
            current_user = UserModel.query.filter_by(_uid=uid).first()
        except jwt.DecodeError:
            flash('Error decoding your token please login again')
            return redirect(url_for('users.login'))
        except Exception as e:
            flash('Unable to locate your account please create a new account')
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
                    current_user = UserModel.query.filter_by(_uid=uid).first()
                    return f(current_user, *args, **kwargs)
                except jwt.DecodeError as e:
                    # If user not logged in do nothing
                    pass
            else:
                pass
        return f(current_user, *args, **kwargs)

    return decorated


def is_authenticated(token):
    try:
        uid = decode_auth_token(auth_token=token)
        current_user = UserModel.query.filter_by(_uid=uid).first()
        return True
    except jwt.DecodeError as e:
        return False


def authenticated_user(token):
    try:
        uid = decode_auth_token(auth_token=token)
        current_user = UserModel.query.filter_by(_uid=uid).first()
        return current_user
    except jwt.DecodeError as e:
        return None



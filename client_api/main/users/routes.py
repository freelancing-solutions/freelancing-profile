from flask import render_template, Blueprint, request, abort, make_response, jsonify, redirect, url_for
from flask_login import login_user,logout_user,login_required
from ..library import Metatags, encode_auth_token, token_required
from .models import UserModel
from .. import db
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('auth/login.html',
                                menu_open=True,
                                meta_tags=Metatags().set_login())
    elif request.method == 'POST':
        auth = request.get_json()
        if not auth or not auth['username'] or not auth['password']:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user_model = UserModel.query.filter_by(username=auth['username']).first()
        if not user_model:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if check_password_hash(user_model.password,auth['password']):
            token = encode_auth_token(uid=user_model.uid)
            # print('----------')
            # print('token : {}'.format(token))
            return jsonify({'token': token})
        else:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@users.route('/logout', methods=['GET', 'POST'])
@token_required
def logout(current_user):
    return render_template('auth/logout.html', current_user=current_user, heading="Log Out", menu_open=True, meta_tags=Metatags().set_logout())


@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('auth/register.html', heading="Register", menu_open=True,
                            meta_tags=Metatags().set_register())
    elif request.method == "POST":
        user_details = request.get_json()
        if user_details and 'email' in user_details:
            email = user_details['email']
        else:
            return jsonify({'message': 'email address is required'})
        if user_details and 'password' in user_details:
            password = user_details['password']
        else:
            return jsonify({'message': 'password is required'})
        if user_details and 'names' in user_details:
            names = user_details['names']
            # NOTE : attempt names surname detection and resolution
        else:
            return jsonify({'message': 'names is required'})

        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            return jsonify({'message': 'User already exists'})


        password_hash = generate_password_hash(password=password,method='sha256')
        uid = str(uuid.uuid4())
        user_model - UserModel(uid=uid ,username=email,email=email,password=password_hash,names=names,admin=False)
        db.session.add(user_model)
        db.session.commit()
        token = encode_auth_token(uid=user_model.uid)
        return jsonify({'Message':'Successfully created new user', 'token': token})

@users.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('auth/forgot-password.html', heading="Forgot Password", menu_open=True,
                           meta_tags=Metatags().set_register())


@users.route('/recover-password/<path:path>', methods=['GET', 'POST'])
def recover(path):
    return render_template('auth/recover-password.html', heading="Recover Password", menu_open=True,
                           meta_tags=Metatags().set_register())


@users.route('/user/admin', methods=['GET', 'POST'])
@token_required
def useradmin(current_user):
    """
        GIVEN current_user details load user details
        Args:
            current_user ([type]): [description]
    """
    return render_template('user-admin.html', heading='Welcome {}'.format(current_user.names), menu_open=True, meta_tags=Metatags().set_home())
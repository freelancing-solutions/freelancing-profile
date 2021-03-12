from flask import (render_template, Blueprint, request, abort, make_response, jsonify,redirect, url_for, flash , get_flashed_messages)
from flask_login import login_user,logout_user,login_required
from ..library import Metatags, encode_auth_token, token_required, logged_user
from .models import UserModel
from .. import db
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
@logged_user
def login(current_user):
    get_flashed_messages()
    if current_user and current_user.uid:
        #TODO- Redirect to logout page user has already been logged in
        flash(message="you are already logged in", category="warning")
        return redirect(url_for('users.logout'))

    if request.method == "GET":
        return render_template('auth/login.html',
                                menu_open=True,
                                meta_tags=Metatags().set_login())
    elif request.method == 'POST':
        auth = request.get_json()
        print("auth record : {}".format(auth['email']))
        print("auth record : {}".format(auth['password']))
        if not auth or not auth['email'] or not auth['password']:
            return jsonify({"message": "Email and Password are required"}), 401
        email = str(auth['email'])
        user_model = UserModel.query.filter_by(email=email).first()
        if not user_model:
            return jsonify({"message": "User not found"}), 401

        if check_password_hash(user_model.password,auth['password']):
            token = encode_auth_token(uid=user_model.uid)
            return jsonify({'token': token,'message':"you have successfully logged in"}), 200
        else:
            return jsonify({"message": "Passwords do not match"}), 401


@users.route('/logout', methods=['GET', 'POST'])
@token_required
def logout(current_user):
    get_flashed_messages()
    if current_user and current_user.uid:
        return render_template('auth/logout.html', current_user=current_user, heading="Log Out", menu_open=True, meta_tags=Metatags().set_logout())
    else:
        flash(message="you are already logged out", category="warning")
        return redirect(url_for('main.home'))


@users.route('/register', methods=['GET', 'POST'])
@logged_user
def register(current_user):
    get_flashed_messages()
    if current_user and current_user.uid:
        #TODO- Redirect to logout page user has already been logged in
        flash(message="You are already logged in", category="warning")
        return redirect(url_for('users.logout'))


    if request.method == "GET":
        return render_template('auth/register.html', heading="Register", menu_open=True,
                            meta_tags=Metatags().set_register())
    elif request.method == "POST":
        user_details = request.get_json()
        if user_details and 'email' in user_details:
            email = user_details['email']
        else:
            return jsonify({'message': 'Email address is required'})

        if user_details and 'cell' in user_details:
            cell = user_details['cell']
        else:
            return jsonify({'message': 'Cell Number is required'})

        if user_details and 'password' in user_details:
            password = user_details['password']
        else:
            return jsonify({'message': 'Password is required'})

        if user_details and 'names' in user_details:
            names = user_details['names']

        else:
            return jsonify({'message': 'Names is required'})

        if user_details and 'surname' in user_details:
            surname = user_details['surname']
        else:
            return jsonify({'message': 'Surname is required'})

        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            return jsonify({'message': 'User already exists'})


        # TODO check if uid is not present right now
        user_model = UserModel(username=email,email=email,cell=cell,password=password,names=names,surname=surname)
        db.session.add(user_model)
        db.session.commit()
        token = encode_auth_token(uid=user_model.uid)
        return jsonify({'Message':'Successfully created new user', 'token': token})

@users.route('/forgot-password', methods=['GET', 'POST'])
@logged_user
def forgot_password(current_user):
    get_flashed_messages()
    if current_user and current_user.uid:
        flash(message="you are already logged in", category="warning")
        return redirect(url_for('users.logout'))

    return render_template('auth/forgot-password.html', heading="Forgot Password", menu_open=True,
                           meta_tags=Metatags().set_register())


@users.route('/recover-password/<path:path>', methods=['GET', 'POST'])
@logged_user
def recover(current_user,path):
    get_flashed_messages()
    if current_user and current_user.uid:
        flash(message="you are already logged in", category="warning")
        redirect(url_for('users.logout'))
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
    get_flashed_messages()
    return render_template('user-admin.html', heading='Welcome {}'.format(current_user.names), menu_open=True, meta_tags=Metatags().set_home())
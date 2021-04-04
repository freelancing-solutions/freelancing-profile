from flask import (render_template, Blueprint, request, jsonify, redirect, url_for,
                   flash, get_flashed_messages, current_app)
from ..library import Metatags, encode_auth_token, token_required, logged_user
from .models import UserModel
from .. import db
from werkzeug.security import check_password_hash
from sqlalchemy.exc import OperationalError, DisconnectionError, IntegrityError

users = Blueprint('users', __name__, static_folder="../static", template_folder="../templates")


@users.route('/login', methods=['GET', 'POST'])
@logged_user
def login(current_user: any) -> tuple:
    get_flashed_messages()
    if current_user and current_user.uid:
        # TODO- Redirect to logout page user has already been logged in
        flash(message="you are already logged in", category="warning")
        return redirect(url_for('users.logout'))

    if request.method == "GET":
        return render_template('auth/login.html', menu_open=True, meta_tags=Metatags().set_login())

    elif request.method == 'POST':
        auth: dict = request.get_json()
        if not auth or not auth['email'] or not auth['password']:
            return jsonify({"message": "Email and Password are required"}), 401
        email: str = str(auth['email'])

        try:
            user_model: UserModel = UserModel.query.filter_by(_email=email).first()
            if not user_model or (user_model.uid is None):
                return jsonify({"message": "User not found"}), 401

            if check_password_hash(user_model.password, auth['password']):
                token = encode_auth_token(uid=user_model.uid)
                return jsonify({'token': token, 'message': "you have successfully logged in"}), 200
            else:
                return jsonify({"message": "Passwords do not match"}), 401
        except OperationalError as e:
            return jsonify({'status': 'failure', 'message': 'Database error'}), 500
        except DisconnectionError as e:
            return jsonify({'status': 'failure', 'message': 'Error connecting to database'}), 500


@users.route('/logout', methods=['GET', 'POST'])
@token_required
def logout(current_user: any) -> tuple:
    """
        TODO - implement logout procedures
    :param current_user:
    :return:
    """
    get_flashed_messages()
    if current_user and current_user.uid:
        if request.method == "GET":
            # Log off is handled in the front-end through javascript and service worker
            return render_template('auth/logout.html', current_user=current_user, heading="LogOut", menu_open=True,
                                   meta_tags=Metatags().set_logout()), 200
        else:
            # TODO- consider cleanup operations the user is logging off
            pass
    else:
        flash(message="you are already logged out", category="warning")
        return redirect(url_for('main.home')), 200


@users.route('/register', methods=['GET', 'POST'])
@logged_user
def register(current_user: any) -> tuple:
    """
         given that the user is not already logged in,
         a registration form is presented to the user, once submitted new user is created
         and logged in , and a JWT Token submitted as response

        :param current_user:
        :return: token
    """
    get_flashed_messages()
    if current_user and current_user.uid:
        # TODO- Redirect to logout page user has already been logged in
        flash(message="You are already logged in", category="warning")
        return redirect(url_for('users.logout'))

    if request.method == "GET":
        return render_template('auth/register.html', heading="Register", menu_open=True,
                               meta_tags=Metatags().set_register()), 200
    elif request.method == "POST":
        user_details: dict = request.get_json()
        if user_details and ('email' in user_details) and not(user_details['email'].strip() == ""):
            email: str = user_details['email'].strip()
        else:
            return jsonify({'message': 'Email address is required'}), 401
        if 'cell' in user_details and not (user_details['cell'].strip() == ""):
            cell: str = user_details['cell'].strip()
        else:
            return jsonify({'message': 'Cell Number is required'}), 401
        if 'password' in user_details and not(user_details['password'].strip() == ""):
            password: str = user_details['password'].strip()
        else:
            return jsonify({'message': 'Password is required'}), 401
        if 'names' in user_details and not(user_details['names'].strip() == ""):
            names: str = user_details['names'].strip()
        else:
            return jsonify({'message': 'Names is required'}), 401
        if 'surname' in user_details and not (user_details['surname'].strip() == ""):
            surname: str = user_details['surname'].strip()
        else:
            return jsonify({'message': 'Surname is required'}), 401

        try:
            user_model: UserModel = UserModel.query.filter_by(_email=email).first()
        except OperationalError as e:
            return jsonify({'status': 'failure', 'message': 'Database error'}), 500
        except DisconnectionError as e:
            return jsonify({'status': 'failure', 'message': 'Error connecting to database'}), 500

        if user_model and user_model.uid:
            return jsonify({'message': 'Email address already used to register an account Please Login'}), 500

        try:
            user_model: UserModel = UserModel(username=email, email=email, cell=cell, password=password, names=names,
                                              surname=surname)
            db.session.add(user_model)
            db.session.commit()
            token = encode_auth_token(uid=user_model.uid)
        except OperationalError as e:
            return jsonify({'status': 'failure', 'message': 'Database error'}), 500
        except DisconnectionError as e:
            return jsonify({'status': 'failure', 'message': 'Error connecting to database'}), 500

        return jsonify({'Message': 'Successfully created new user', 'token': token}), 500


@users.route('/forgot-password', methods=['GET', 'POST'])
@logged_user
def forgot_password(current_user: any) -> tuple:
    """
            TODO- implement password recovery procedures
        :param current_user:
        :return: present to user a screen allowing the user to input the email connected to the account.
        send a recovery email containing password recovery token.
    """
    get_flashed_messages()
    if current_user and current_user.uid:
        flash(message="you are already logged in", category="warning")
        return redirect(url_for('users.logout'))

    return render_template('auth/forgot-password.html', heading="Forgot Password", menu_open=True,
                           meta_tags=Metatags().set_register()), 200


@users.route('/recover-password/<path:path>', methods=['GET', 'POST'])
@logged_user
def recover(current_user: any, path: str) -> tuple:
    """
        :param current_user: if logged in current user will be contained here
        :param path: contains recovery token - use the token to determine if the request was valid
        :return: a screen displaying if the password recovery was a success
    """
    get_flashed_messages()
    if current_user and current_user.uid:
        flash(message="you are already logged in", category="warning")
        redirect(url_for('users.logout'))
    # TODO- perform recovery operation here if successful, present the user with a screen asking for the new password
    # Once successful submit a response indicating this condition and also login the user
    if request.method == "GET":
        recovery_token: str = path
        # TODO- create a proper password recovery procedure
        return render_template('auth/recover-password.html', heading="Recover Password", menu_open=True,
                               meta_tags=Metatags().set_register()), 200

    elif request.method == "POST":
        new_account: dict = request.get_json()
        if 'password' in new_account or new_account['password'].strip() == "":
            return jsonify({'status': 'failure', 'message': 'password is required'}), 500
        if 'email' in new_account or new_account['email'].strip() == "":
            return jsonify({'status': 'failure', 'message': 'email is required'}), 500

        password: str = new_account['password'].strip()
        email: str = new_account['email'].strip()

        try:

            user_account_instance: UserModel = UserModel.query.filter_by(_email=email).first()
            if user_account_instance and user_account_instance.uid:
                user_account_instance.password = password
                db.session.update(user_account_instance)
                db.session.commit()
                return jsonify({'message': 'Password successfully changed',
                                'token': encode_auth_token(user_account_instance.uid)}), 200
            else:
                return jsonify({'message': 'User nor found'}), 401
        except OperationalError as e:
            return jsonify({'status': 'failure', 'message': 'Database error'}), 500
        except DisconnectionError as e:
            return jsonify({'status': 'failure', 'message': 'Error connecting to database'}), 500


@users.route('/user/admin', methods=['GET', 'POST'])
@token_required
def user_admin(current_user: any) -> tuple:
    """
        GIVEN current_user details load user details
        Args:
            current_user ([type]): [description]
    """
    get_flashed_messages()
    return render_template('user-admin.html', heading='Welcome {}'.format(current_user.names),
                           menu_open=True, meta_tags=Metatags().set_home()), 200

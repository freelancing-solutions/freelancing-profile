from flask import render_template, Blueprint, request, abort
from flask_login import login_user,logout_user,login_required
from main.library import Metatags
users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('auth/login.html',
                                menu_open=True,
                                meta_tags=Metatags().set_login())

@users.route('/logout', methods=['GET'])
def logout():
    return render_template('auth/logout.html', heading="Log Out", menu_open=True, meta_tags=Metatags().set_logout())


@users.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html', heading="Register", menu_open=True,
                           meta_tags=Metatags().set_register())


@users.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('auth/forgot-password.html', heading="Forgot Password", menu_open=True,
                           meta_tags=Metatags().set_register())


@users.route('/recover-password/<path:path>', methods=['GET', 'POST'])
def recover(path):
    return render_template('auth/recover-password.html', heading="Recover Password", menu_open=True,
                           meta_tags=Metatags().set_register())



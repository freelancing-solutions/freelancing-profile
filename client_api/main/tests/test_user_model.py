import uuid, time

from sqlalchemy.exc import OperationalError

from .. import db, create_app
from flask import current_app
from ..library.utils import create_id


def test_add_user_through_rest_api():
    from ..rest_api import UserAPI
    from ..users.models import UserModel

    if not current_app:
        app = create_app()
        app.app_context().push()
    else:
        app = current_app

    username = "{}@gmail.com".format(str(create_id()))
    email = "{}@gmail.com".format(str(create_id()))
    password = "mobius"
    names = "mobius"
    surname = "crypt"
    admin = True
    img_link = "https://justice-ndou.appspot.com/static/dist/img/justice.jpg"

    cell = "0764567890"
    with app.app_context():
        user_model_instance = UserModel(username=username, email=email, password=password, names=names, surname=surname,
                                        cell=cell, admin=admin, img_link=img_link)
        try:
            db.session.add(user_model_instance)
            db.session.commit()
        except OperationalError as error:
            db.session.rollback()
            db.session.commit()

        assert isinstance(user_model_instance, UserModel), "User model not instantiating correctly"
        assert user_model_instance.uid, "UID not set correctly"
        assert user_model_instance.username == username, "Username not set correctly"
        assert user_model_instance.email == email, "Email not set Correctly"
        assert user_model_instance.password, "password hash not set correctly"
        assert user_model_instance.names == names, "Names not set correctly"
        assert user_model_instance.surname == surname, "Surname not set correctly"
        assert user_model_instance.admin == admin, "Admin not set correctly"
        assert user_model_instance.img_link == img_link, "img_link not set correctly"

        user_model_recalled = UserModel.query.filter_by(_email=email).first()
        assert user_model_recalled, "Unable to recall user model from database"
        assert user_model_recalled == user_model_instance, "UserModel from database is being modified"


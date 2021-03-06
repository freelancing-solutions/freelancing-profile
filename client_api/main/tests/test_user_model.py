import uuid, time
from .. import db, create_app
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

def test_add_user_through_rest_api():
    from ..rest_api import UserAPI
    from ..users.models import UserModel

    if not current_app:
        app = create_app()
        app.app_context().push()
    else:
        app = current_app

    uid = str(uuid.uuid4())
    username = "mobius-crypt{}".format(str(uuid.uuid1()))
    email = "mobius-crypt{}@gmail.com".format(str(uuid.uuid1()))
    password_hash = generate_password_hash("mobius1234567",method="sha256")
    names="mobius"
    surname="crypt"
    admin=True
    img_link="https://justice-ndou.appspot.com/static/dist/img/justice.jpg"

    cell = "0764567890"

    with app.app_context():

        user_model_instance = UserModel(uid=uid,username=username,email=email,password=password_hash,names=names,surname=surname,cell=cell,admin=admin,img_link=img_link)
        try:
            db.session.add(user_model_instance)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            db.session.commit()


        assert isinstance(user_model_instance,UserModel), "User model not instantiating correctly"
        assert user_model_instance.uid == uid, "UID not set correctly"
        assert user_model_instance.username == username, "Username not set correctly"
        assert user_model_instance.email == email, "Email not set Correctly"
        assert user_model_instance.password == password_hash, "password hash not set correctly"
        assert user_model_instance.names == names, "Names not set correctly"
        assert user_model_instance.surname == surname, "Surname not set correctly"
        assert user_model_instance.admin == admin, "Admin not set correctly"
        assert user_model_instance.img_link == img_link, "img_link not set correctly"

        user_model_recalled = UserModel.query.filter_by(uid=uid).first()
        assert user_model_recalled, "Unable to recall user model from database"
        assert user_model_recalled == user_model_instance, "UserModel from database is being modified"


import uuid, time
from .. import db, create_app
from flask import current_app, jsonify
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
        # TODO- Create a test case by calling the User API Restful Api with the above data
        data = jsonify({
                "username":username,"email":email,"password":"mobius1234567",
                "names":names,"surname":surname,"admin":admin,"img_link":img_link
            })

        api_instance = UserAPI()
        api_instance.dispatch_request()
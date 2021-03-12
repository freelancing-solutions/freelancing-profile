from .. import db
from flask import current_app
from werkzeug.security import generate_password_hash
import uuid
class UserModel(db.Model):
    uid = db.Column(db.String(36),unique=True,primary_key=True) # Public ID
    username = db.Column(db.String(128), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    names = db.Column(db.String(128), nullable=True)
    surname = db.Column(db.String(128), nullable=True)
    cell = db.Column(db.String(13), nullable=True)
    admin = db.Column(db.Boolean, default=False)
    img_link = db.Column(db.String(256), nullable=True)

    def __init__(self, username,email,password,names,surname,cell,admin=False,img_link=None):
        self.uid = str(uuid.uuid4())
        self.img_link = img_link
        if username:
            self.username = username
        else:
            self.username = email
        self.email = email
        self.password = generate_password_hash(password,method='sha256')
        self.names = names
        self.surname = surname
        self.cell = cell
        self.admin = admin
        self.img_link = img_link
        super(UserModel,self).__init__()

    def __repr__(self):
        return '<User {}> <Email {}>'.format(self.username,self.email)


    def __eq__(self, value):
        if value is None:
            return False
        if (self.uid == value.uid) and (self.username == value.username) and (self.email == value.email) and (self.password == value.password) and (self.names == value.names) and \
        (self.surname == value.surname) and (self.cell == value.cell) and (self.admin == value.admin) and (self.img_link == value.img_link):
            return True

        return False

    @staticmethod
    def add_user(uid,email,username=None,names=None,surname=None,cell=None):
        user = UserModel(uid=uid,email=email,username=username,names=names,surname=surname,cell=cell)
        db.session.add(user)
        db.session.commit()
        return True






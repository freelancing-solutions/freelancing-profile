from .. import db
from flask import current_app

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(128),unique=True) # Public ID
    username = db.Column(db.String(128), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    names = db.Column(db.String(128), nullable=True)
    surname = db.Column(db.String(128), nullable=True)
    cell = db.Column(db.String(13), nullable=True)
    admin = db.Column(db.Boolean)
    img_link = db.Column(db.String(256), nullable=True)

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






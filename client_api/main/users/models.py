from main import db
from flask import current_app

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(128),unique=True)
    username = db.Column(db.String(128), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    names = db.Column(db.String(128), nullable=True)
    surname = db.Column(db.String(128), nullable=True)
    cell = db.Column(db.String(13), nullable=True)

    def __repr__(self):
        return '<User {}> <Email {}>'.format(self.username,self.email)

    @staticmethod
    def add_user(uid,email,username=None,names=None,surname=None,cell=None):
        user = UserModel(uid=uid,email=email,username=username,names=names,surname=surname,cell=cell)
        db.session.add(user)
        db.session.commit()
        return True






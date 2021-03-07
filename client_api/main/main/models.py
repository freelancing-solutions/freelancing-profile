from .. import db
from flask import current_app


class ContactModel(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True, unique=True)
    uid = db.Column(db.String(128), unique=True, nullable=True)
    names = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), unique=False, nullable=False)
    cell = db.Column(db.String(13), unique=False, nullable=False)
    subject = db.Column(db.String(256), unique=False, nullable=False)
    body = db.Column(db.String(2048), unique=False, nullable=False)
    reason = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(self, uid, names, email, cell, subject, body,reason):
        self.uid = uid
        self.names = names
        self.email = email
        self.cell = cell
        self.reason = reason
        self.subject = subject
        self.body = body


    def __repr__(self):
        return '<ContactModel names : {}, email: {}, cell: {}, subject: {}, body: {}, reason: {}>'.format(self.names,self.email,self.cell,self.subject,self.body,self.reason)

    def __eq__(self, value):
        if (value.uid == self.uid) and (value.names == self.names) and  (value.email == self.email) and (value.cell == self.cell) and (value.subject == self.subject) and (value.body == self.body) and (value.reason == self.reason):
            return True
        return False


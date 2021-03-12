from .. import db
from flask import current_app
import uuid


class ContactModel(db.Model):
    _contact_id = db.Column(db.String(36), primary_key=True, unique=True)
    _uid = db.Column(db.String(36), unique=True, nullable=True)
    _names = db.Column(db.String(128), unique=False, nullable=False)
    _email = db.Column(db.String(128), unique=False, nullable=False)
    _subject = db.Column(db.String(256), unique=False, nullable=False)
    _body = db.Column(db.String(2048), unique=False, nullable=False)
    _reason = db.Column(db.String(128), unique=False, nullable=False)

    @property
    def contact_id(self):
        return self._contact_id

    @contact_id.setter
    def contact_id(self, contact_id):
        if (contact_id is None):
            raise ValueError('contact_id can only be a uuid string')

        if not isinstance(contact_id, str):
            raise TypeError('contact_id is not a string')

        if len(contact_id) > 36:
            raise ValueError('incorrect value format contact_id')

        self._contact_id = contact_id

    @property
    def uid(self):
        if self._uid is None:
            raise ValueError('uid is not set')
        return self._uid

    @uid.setter
    def uid(self,uid):
        if (uid is None):
            raise ValueError('uid cannot be null')

        if not isinstance(uid,str):
            raise TypeError('uid is not a string')

        if len(uid) > 36:
            raise ValueError("incorrect format for uid")

        self._uid = uid


    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, names):
        if (names is None):
            raise ValueError('names cannot be null')

        if not isinstance(names, str):
            raise TypeError("Names is not a string")

        if len(names) > 128:
            raise ValueError("Names field is too long please enter proper names")

        self._names = names

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self,email):
        if (email is None):
            raise ValueError('Email cannot be None')
        if not isinstance(email, str):
            raise TypeError("Email can only be a string")

        # TODO- check email format

        if len(email) > 128:
            raise ValueError('email is too long please provide proper email fields')

        self._email = email

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self,subject):
        if (subject is None):
            raise ValueError("Subject cannot be null")
        if not isinstance(subject,str):
            raise TypeError("Subject can only be a string")

        self._subject = subject

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self,body):
        if (body is None):
            raise ValueError("Body cannot be null")
        if not isinstance(body,str):
            raise TypeError("Body can only be a string")

        self._body = body

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self,reason):
        if reason is None:
            raise ValueError("Reason cannot be null")

        if not isinstance(reason,str):
            raise TypeError("Reason can only be a string")

        self._reason = reason



    def __init__(self,  names, email, cell, subject, body, reason,uid=None):
        self.contact_id = str(uuid.uuid4())
        if uid:
            self.uid = uid
        self.names = names
        self.email = email
        self.cell = cell
        self.reason = reason
        self.subject = subject
        self.body = body
        super(ContactModel,self).__init__()

    def __repr__(self):
        return '<ContactModel names : {}, email: {}, cell: {}, subject: {}, body: {}, reason: {}>'.format(self.names,self.email,self.cell,self.subject,self.body,self.reason)

    def __eq__(self, value):
        if (value.uid == self.uid) and (value.names == self.names) and  (value.email == self.email) and (value.cell == self.cell) and (value.subject == self.subject) and (value.body == self.body) and (value.reason == self.reason):
            return True
        return False


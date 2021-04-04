import time
import uuid

from sqlalchemy.exc import OperationalError

from .. import db
from ..library.utils import timestamp, create_id, const


class ContactModel(db.Model):
    __bind_key__ = "app"
    _contact_id = db.Column(db.String(const.uuid_len), primary_key=True, unique=True)
    _uid = db.Column(db.String(const.uuid_len), unique=False, nullable=True)
    _names = db.Column(db.String(const.names_len), unique=False, nullable=False)
    _email = db.Column(db.String(const.email_len), unique=False, nullable=False)
    _subject = db.Column(db.String(const.subject_len), unique=False, nullable=False)
    _body = db.Column(db.String(const.body_len), unique=False, nullable=False)
    _reason = db.Column(db.String(const.reason_len), unique=False, nullable=False)
    _time_created = db.Column(db.Integer, default=timestamp())
    _is_read = db.Column(db.Boolean, default=False)
    _time_read = db.Column(db.Integer, default=0, onupdate=timestamp())
    _responses = db.relationship('ResponseModel', backref=db.backref('contact_message', lazy=True))

    @property
    def time_created(self) -> int:
        return self._time_created

    @time_created.setter
    def time_created(self, time_created: int) -> None:
        if time_created is None:
            raise ValueError('Time created cannot be null')
        if not isinstance(time_created, int):
            raise TypeError('Time Created can only be an integer')

        self._time_created = time_created

    @property
    def is_read(self) -> bool:
        return self._is_read

    @is_read.setter
    def is_read(self, is_read: bool) -> None:
        if not isinstance(is_read, bool):
            raise TypeError('Is_read can only be a Boolean')
        self._is_read = is_read

    @property
    def time_read(self) -> int:
        return self._time_read

    @time_read.setter
    def time_read(self, time_read: int) -> None:
        if time_read is None:
            raise ValueError('Time is read cannot be Null')
        if not isinstance(time_read, int):
            raise TypeError('Time read can only be an integer')

        self._time_read = time_read

    @property
    def contact_id(self) -> str:
        return self._contact_id

    @contact_id.setter
    def contact_id(self, contact_id: str) -> None:
        if contact_id is None:
            raise ValueError('contact_id can only be a uuid string')

        if not isinstance(contact_id, str):
            raise TypeError('contact_id is not a string')

        if len(contact_id) > const.uuid_len:
            raise ValueError('incorrect value format contact_id')

        self._contact_id = contact_id

    @property
    def uid(self) -> str:
        if self._uid is None:
            raise ValueError('uid is not set')
        return self._uid

    @uid.setter
    def uid(self, uid: str) -> None:
        if uid is None:
            raise ValueError('uid cannot be null')

        if not isinstance(uid, str):
            raise TypeError('uid is not a string')

        if len(uid) > const.uuid_len:
            raise ValueError("incorrect format for uid")

        self._uid = uid

    @property
    def names(self) -> str:
        return self._names

    @names.setter
    def names(self, names: str) -> None:
        if names is None:
            raise ValueError('names cannot be null')

        if not isinstance(names, str):
            raise TypeError("Names is not a string")

        if len(names) > 128:
            raise ValueError("Names field is too long please enter proper names")

        self._names = names

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        if email is None:
            raise ValueError('Email cannot be None')
        if not isinstance(email, str):
            raise TypeError("Email can only be a string")

        # TODO- check email format

        if len(email) > const.email_len:
            raise ValueError('email is too long please provide proper email fields')

        self._email = email

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, subject: str) -> None:
        if subject is None:
            raise ValueError("Subject cannot be null")
        if not isinstance(subject, str):
            raise TypeError("Subject can only be a string")

        self._subject = subject

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, body: str) -> None:
        if body is None:
            raise ValueError("Body cannot be null")
        if not isinstance(body, str):
            raise TypeError("Body can only be a string")

        self._body = body

    @property
    def reason(self) -> str:
        return self._reason

    @reason.setter
    def reason(self, reason: str) -> None:
        if reason is None:
            raise ValueError("Reason cannot be null")

        if not isinstance(reason, str):
            raise TypeError("Reason can only be a string")

        self._reason = reason

    def __init__(self, names: str, email: str, cell: str, subject: str, body: str, reason: str,
                 uid: str = None):
        self.contact_id = str(uuid.uuid4())
        super(ContactModel, self).__init__()
        if uid is not None:
            self.uid = uid
        self.names = names
        self.email = email
        self.cell = cell
        self.reason = reason
        self.subject = subject
        self.body = body

    def __repr__(self) -> str:
        return '<ContactModel names : {}, email: {}, ' \
               'cell: {}, subject: {}, body: {}, reason: {}>'.format(self.names, self.email, self.cell,
                                                                     self.subject, self.body, self.reason)

    def __eq__(self, value) -> bool:
        """
            :type value: self
            :param value: value
            :return: bool
        """
        if (value.uid == self.uid) and (value.names == self.names) and (value.email == self.email) and \
                (value.cell == self.cell) and (value.subject == self.subject) and (value.body == self.body) \
                and (value.reason == self.reason):
            return True
        return False


class ResponseModel(db.Model):
    """
        a model to represent admin responses
    """
    _contact_id = db.Column(db.String(const.uuid_len), db.ForeignKey('contact_model._contact_id'), unique=False,
                            nullable=False)
    _response_id = db.Column(db.String(const.uuid_len), primary_key=True, unique=True)
    _subject = db.Column(db.String(const.subject_len), nullable=False)
    _response = db.Column(db.String(const.response_len), nullable=False)
    _time_created = db.Column(db.Integer, nullable=False, default=timestamp())
    _is_sent_by_email = db.Column(db.Boolean, default=False)
    _is_issue_resolved = db.Column(db.Boolean, default=False)

    @property
    def contact_id(self) -> str:
        """
            :return contact_id:
        """
        return self._contact_id

    @contact_id.setter
    def contact_id(self, contact_id: str) -> None:
        """
            :param contact_id:
            :return Null:
        """
        if contact_id is None:
            raise ValueError('Contact ID is Null')

        if not isinstance(contact_id, str):
            raise TypeError('Contact ID can only be a string')

        self._contact_id = contact_id

    @property
    def response_id(self) -> str:
        """
            :return response_id:
        """
        return self._response_id

    @response_id.setter
    def response_id(self, response_id: str) -> None:
        """
            :param response_id:
            :return Null:
        """
        if response_id is None:
            raise ValueError('Response ID is Null')
        if not isinstance(response_id, str):
            raise TypeError('Response ID can only ')

    @property
    def subject(self) -> str:
        """
            :return subject:
        """
        return self._subject

    @subject.setter
    def subject(self, subject: str) -> None:
        """
            :param subject:
            :return Null:
        """
        if subject is None:
            raise ValueError('Subject is Null')
        if not isinstance(subject, str):
            raise TypeError('Subject can only be a string')
        self._subject = subject

    @property
    def response(self) -> str:
        """
            :return response:
        """
        return self._response

    @response.setter
    def response(self, response: str) -> None:
        """
            :param response:
            :return Null:
        """
        if response is None:
            raise ValueError('Response is Null')
        if not isinstance(response, str):
            raise TypeError('Response can only be a string')
        self._response = response

    @property
    def time_created(self) -> int:
        """
            :return time_created:
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created: int) -> None:
        """
            :param time_created:
            :return Null:
        """
        if time_created is None:
            raise ValueError('Time Created is Null')

        if not isinstance(time_created, int):
            raise TypeError('Time Created can only be a string')
        self._time_created = time_created

    @property
    def is_sent_by_email(self) -> bool:
        """
            :return is_sent_by_email:
        """
        return self._is_sent_by_email

    @is_sent_by_email.setter
    def is_sent_by_email(self, is_sent_by_email: bool) -> None:
        """
            :param is_sent_by_email:
            :return Null:
        """
        if not isinstance(is_sent_by_email, bool):
            raise TypeError('is sent by email can only be a boolean')
        self._is_sent_by_email = is_sent_by_email

    @property
    def is_issue_resolved(self) -> bool:
        """
            :return issue_resolved:
        """
        return self._is_issue_resolved

    @is_issue_resolved.setter
    def is_issue_resolved(self, is_issue_resolved: bool) -> None:
        if not isinstance(is_issue_resolved, bool):
            raise TypeError('Is Issue Resolved can only be a Boolean')

        self._is_issue_resolved = is_issue_resolved

    def __init__(self, subject: str, response: str, contact_id: str):
        self.contact_id = contact_id
        self.response_id = str(uuid.uuid4())
        self.subject = subject
        self.response = response
        super(ResponseModel, self).__init__()

    def __eq__(self, response) -> bool:
        if (response.subject == self.subject) and (response.response == self.response) and \
                (response.contact_id == self.contact_id):
            return True
        return False

    def __repr__(self) -> str:
        return "<Response Subject : {}, Response: {}>".format(self.subject, self.response)


def attach_orphaned_records_to_accounts() -> None:
    """
        :return: null
    """
    from ..users.models import UserModel
    try:
        contacts_list = ContactModel.query.filter_by(_uid="").all()
        for contact in contacts_list:
            user = UserModel.get_user_by_email(email=contact.email)
            if user and user.uid:
                contact.uid = user.uid
                db.session.add(contact)
        db.session.commit()
    except OperationalError as e:
        pass

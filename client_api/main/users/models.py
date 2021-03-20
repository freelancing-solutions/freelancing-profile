import uuid
import time
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..library.utils import const, create_id, timestamp


class UserModel(db.Model):
    """
        to access freelance jobs use relationship freelancejobs a list[]
        to access payments use relationship = payments a list[]
    """
    _uid = db.Column(db.String(const.uuid_len), unique=True, primary_key=True)
    _username = db.Column(db.String(const.username_len), unique=True, nullable=True)
    _email = db.Column(db.String(const.username_len), unique=True, nullable=False)
    _password = db.Column(db.String(const.password_len))
    _names = db.Column(db.String(const.names_len), nullable=True)
    _surname = db.Column(db.String(const.names_len), nullable=True)
    _cell = db.Column(db.String(const.cell_len), nullable=True)
    _admin = db.Column(db.Boolean, default=False)
    _img_link = db.Column(db.String(const.link_len), nullable=True)
    _time_registered = db.Column(db.Integer, nullable=False, default=timestamp())
    _time_email_verified = db.Column(db.Integer, nullable=False, default=0)
    _time_cell_verified = db.Column(db.Integer, nullable=False, default=0)
    _email_is_verified = db.Column(db.Boolean, nullable=False, default=False)
    _cell_is_verified = db.Column(db.Boolean, nullable=False, default=False)
    _freelancejobs = db.relationship('FreelanceJobModel', backref=db.backref('user', lazy=True))
    _payments = db.relationship('PaymentModel', backref=db.backref('user', lazy=True))
    _verification_token = db.Column(db.String(const.id_len), unique=True, nullable=True,
                                    default=create_id(size=const.id_len))

    @property
    def uid(self):
        if (len(self._uid) == const.uuid_len) and isinstance(self._uid, str):
            return self._uid
        else:
            return None

    @uid.setter
    def uid(self, uid):
        if uid is None:
            raise ValueError('uid cannot be Null')
        if not isinstance(uid, str):
            raise TypeError("uid can only be a string")
        if len(uid) != 36:
            raise ValueError('invalid uid format')

        self._uid = uid

    @property
    def username(self):
        if self._username is None and (self._email is not None):
            return self._email
        elif self._username:
            return self._username
        else:
            return None

    @username.setter
    def username(self, username):
        if username is None:
            raise ValueError('Username cannot be Null')
        if not isinstance(username, str):
            raise TypeError('Username can only be a string')
        if len(username) > 128:
            raise ValueError('Invalid username format character length exceed 128')

        self._username = username

    @property
    def email(self):
        # TODO- check if its valid email
        return self._email

    @email.setter
    def email(self, email):
        if email is None:
            raise ValueError("Email address cannot be null")
        if not isinstance(email, str):
            raise TypeError('Email can only be a string')

        if len(email) > 128:
            raise ValueError("Invalid Email format character length exceed 128")

        self._email = email

    @property
    def password(self) -> str:
        """
            retrieves password hash
        Returns:
            str: [password hash]
        """
        return self._password

    @password.setter
    def password(self, password):
        """
            Given a plain password convert to password hash and store
        Args:
            password ([str]): [password string]
        Raises:
            ValueError: [password cannot be null]
            TypeError: [password can only be a string]
        """
        if password is None:
            raise ValueError('Password cannot be empty')
        if not isinstance(password, str):
            raise TypeError("password can only be a string")

        self._password = generate_password_hash(password, method='sha256', salt_length=8)

    @property
    def names(self) -> str:
        return self._names

    @names.setter
    def names(self, names):
        if names is None:
            raise ValueError('Names cannot be Null')
        if not isinstance(names, str):
            raise TypeError('Names can only be a string')

        if len(names) > 128:
            raise ValueError('Invalid names format names length exceeds 128')

        self._names = names

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, surname):
        if surname is None:
            raise ValueError('Surname cannot be Null')
        if not isinstance(surname, str):
            raise TypeError('Surname can only be a string')

        if len(surname) > 128:
            raise ValueError('Invalid Surname format names length exceeds 128')

        self._surname = surname

    @property
    def cell(self) -> str:
        return self._cell

    @cell.setter
    def cell(self, cell):
        if cell is None:
            raise ValueError('Cell Number can not be null')
        if not isinstance(cell, str):
            raise TypeError('Cell Can only be a string')

        if len(cell) > 13:
            raise ValueError('Cell Number can not exceed 13 characters')

        self._cell = cell

    @property
    def admin(self) -> bool:
        """
        Returns:
            bool: [is user admin]
        """
        return self._admin

    @admin.setter
    def admin(self, admin):
        if not isinstance(admin, bool):
            raise TypeError('admin can only be a boolean')
        self._admin = admin

    @property
    def img_link(self):
        return self._img_link

    @img_link.setter
    def img_link(self, img_link):
        if img_link is None:
            raise ValueError('Image Link cannot be null')

        if not isinstance(img_link, str):
            raise TypeError('Image link cannot be null')

        self._img_link = img_link

    @property
    def time_registered(self) -> int:
        return self._time_registered

    @time_registered.setter
    def time_registered(self, time_registered):
        if time_registered is None:
            raise ValueError('Time registered can only be an integer')
        if not isinstance(time_registered, int):
            raise TypeError('Time registered can only be an integer')

        self._time_registered = time_registered

    @property
    def time_email_verified(self) -> int:
        return self._time_email_verified

    @time_email_verified.setter
    def time_email_verified(self, time_email_verified):
        if time_email_verified is None:
            raise ValueError('Time email verified is Null')

        if not isinstance(time_email_verified, int):
            raise TypeError('Time email verified can only be integer')

        self._time_email_verified = time_email_verified

    @property
    def time_cell_verified(self) -> int:
        return self._time_cell_verified

    @time_cell_verified.setter
    def time_cell_verified(self, time_cell_verified):
        if time_cell_verified is None:
            raise ValueError('Time cell verified is null')

        if not isinstance(time_cell_verified, int):
            raise TypeError('Time cell verified')

        self._time_cell_verified = time_cell_verified

    @property
    def email_is_verified(self) -> bool:
        return self._email_is_verified

    @email_is_verified.setter
    def email_is_verified(self, email_is_verified):
        if not isinstance(email_is_verified, bool):
            raise TypeError('Email is verified can only be a boolean')

        self._email_is_verified = email_is_verified

    @property
    def cell_is_verified(self) -> bool:
        return self._cell_is_verified

    @cell_is_verified.setter
    def cell_is_verified(self, cell_is_verified):
        if not isinstance(cell_is_verified, bool):
            raise TypeError('Cell is verified can only be a boolean')

        self._cell_is_verified = cell_is_verified

    @property
    def verification_token(self):
        return self._verification_token

    @verification_token.setter
    def verification_token(self):
        self._verification_token = create_id()

    # NOTE ACTIONS
    def compare_password(self, password) -> bool:
        """
        Args:
            password ([str]): [password string to test]

        Raises:
            ValueError: [if password is empty]
            TypeError: [password is not string]

        Returns:
            bool: [True if password matches the password hash]
        """
        if password is None:
            raise ValueError('Password cannot be empty')
        if not isinstance(password, str):
            raise TypeError('Password can only be a string')

        return check_password_hash(self.password, password)

    def is_admin(self) -> bool:
        return self.admin

    def send_email_verification(self):
        # TODO- Use Flask-Email
        pass

    def verify_email(self):
        pass

    def send_cell_verification(self):
        pass

    def verify_cell(self, cell):
        pass

    def __init__(self, username, email, password, names, surname, cell, admin=False, img_link=None):
        self.uid = str(uuid.uuid4())
        if username:
            self.username = username
        else:
            self.username = email
        self.email = email
        self.password = password
        self.names = names
        self.surname = surname
        self.cell = cell
        self.admin = admin
        if img_link:
            self.img_link = img_link
        super(UserModel, self).__init__()

    def __repr__(self):
        return '<User {}> <Email {}>'.format(self.username, self.email)

    def __eq__(self, value):
        if value is None:
            return False
        if (self.uid == value.uid) and (self.username == value.username) and (self.email == value.email) and (
                self.password == value.password) and (self.names == value.names) and \
                (self.surname == value.surname) and (self.cell == value.cell) and (self.admin == value.admin) and (
                self.img_link == value.img_link):
            return True

        return False

    @staticmethod
    def add_user(email, username=None, names=None, surname=None, cell=None):
        user = UserModel(email=email, username=username, names=names, surname=surname, cell=cell)
        db.session.add(user)
        db.session.commit()
        return True

    @classmethod
    def add_freelance_job(cls, uid, freelance_job):
        user_instance = UserModel.query.filter_by(_uid=uid).first()
        user_instance._freelancejobs.append(freelance_job)
        db.session.update(user_instance)
        db.session.commit()

    @classmethod
    def add_payment(cls, uid, payment):
        user_instance = UserModel.query.filter_by(_uid=uid).first()
        user_instance._payments.append(payment)
        db.session.update(user_instance)
        db.session.commit()

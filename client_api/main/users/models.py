import uuid
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..library.utils import const, create_id, timestamp, is_email, is_cell
from sqlalchemy.event import listen
from sqlalchemy.exc import OperationalError, DisconnectionError, IntegrityError


class UserModel(db.Model):
    """
        to access freelance jobs use relationship freelancejobs a list[]
        to access payments use relationship = payments a list[]
    """
    __bind_key__ = "app"
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
    _verification_token = db.Column(db.String(const.id_len), unique=True, nullable=True,
                                    default=create_id(size=const.id_len))
    _cell_verification_token = db.Column(db.String(const.cell_token_len), unique=True, nullable=True,
                                         default=create_id(size=const.cell_token_len))
    _freelancejobs = db.relationship('FreelanceJobModel', backref=db.backref('user', lazy=True))
    _payments = db.relationship('PaymentModel', backref=db.backref('user', lazy=True))

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, uid: str) -> None:
        if uid is None:
            raise ValueError('uid cannot be Null')
        if not isinstance(uid, str):
            raise TypeError("uid can only be a string")
        if len(uid) != const.uuid_len:
            raise ValueError('invalid uid format')

        self._uid = uid

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        if username is None:
            raise ValueError('Username cannot be Null')
        if not isinstance(username, str):
            raise TypeError('Username can only be a string')
        if len(username) > const.username_len:
            raise ValueError('Invalid username format character length exceed 128')
        print('Storing username ', username)
        self._username = username

    @property
    def email(self) -> str:
        # TODO- check if its valid email
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        if email is None:
            raise ValueError("Email address cannot be null")
        if not isinstance(email, str):
            raise TypeError('Email can only be a string')

        if len(email) > const.email_len:
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
    def password(self, password: str) -> None:
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
    def names(self, names: str) -> None:
        if names is None:
            raise ValueError('Names cannot be Null')
        if not isinstance(names, str):
            raise TypeError('Names can only be a string')

        if len(names) > const.names_len:
            raise ValueError('Invalid names format names length exceeds 128')

        self._names = names

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, surname: str) -> None:
        if surname is None:
            raise ValueError('Surname cannot be Null')
        if not isinstance(surname, str):
            raise TypeError('Surname can only be a string')

        if len(surname) > const.names_len:
            raise ValueError('Invalid Surname format names length exceeds 128')

        self._surname = surname

    @property
    def cell(self) -> str:
        return self._cell

    @cell.setter
    def cell(self, cell: str) -> None:
        if cell is None:
            raise ValueError('Cell Number can not be null')
        if not isinstance(cell, str):
            raise TypeError('Cell Can only be a string')

        if len(cell) > const.cell_len:
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
    def admin(self, admin: bool) -> None:
        if not isinstance(admin, bool):
            raise TypeError('admin can only be a boolean')
        self._admin = admin

    @property
    def img_link(self) -> str:
        return self._img_link

    @img_link.setter
    def img_link(self, img_link: str) -> None:
        if img_link is None:
            raise ValueError('Image Link cannot be null')

        if not isinstance(img_link, str):
            raise TypeError('Image link cannot be null')

        self._img_link = img_link

    @property
    def time_registered(self) -> int:
        return self._time_registered

    @time_registered.setter
    def time_registered(self, time_registered: int) -> None:
        if time_registered is None:
            raise ValueError('Time registered can only be an integer')
        if not isinstance(time_registered, int):
            raise TypeError('Time registered can only be an integer')

        self._time_registered = time_registered

    @property
    def time_email_verified(self) -> int:
        return self._time_email_verified

    @time_email_verified.setter
    def time_email_verified(self, time_email_verified: int) -> None:
        if time_email_verified is None:
            raise ValueError('Time email verified is Null')

        if not isinstance(time_email_verified, int):
            raise TypeError('Time email verified can only be integer')

        self._time_email_verified = time_email_verified

    @property
    def time_cell_verified(self) -> int:
        return self._time_cell_verified

    @time_cell_verified.setter
    def time_cell_verified(self, time_cell_verified: int) -> None:
        if time_cell_verified is None:
            raise ValueError('Time cell verified is null')

        if not isinstance(time_cell_verified, int):
            raise TypeError('Time cell verified')

        self._time_cell_verified = time_cell_verified

    @property
    def email_is_verified(self) -> bool:
        return self._email_is_verified

    @email_is_verified.setter
    def email_is_verified(self, email_is_verified: bool) -> None:
        """

        :param email_is_verified: bool
        :return:
        """
        if not isinstance(email_is_verified, bool):
            raise TypeError('Email is verified can only be a boolean')

        self._email_is_verified = email_is_verified

    @property
    def cell_is_verified(self) -> bool:
        """
            cell_is_verified property
            :return: bool
        """
        return self._cell_is_verified

    @cell_is_verified.setter
    def cell_is_verified(self, cell_is_verified: bool) -> None:
        """
            cell_is_verified setter
            :param cell_is_verified: bool
            returns: None
        """
        if not isinstance(cell_is_verified, bool):
            raise TypeError('Cell is verified can only be a boolean')

        self._cell_is_verified = cell_is_verified

    @property
    def verification_token(self) -> str:
        """
            verification_token property
        :return: str
        """
        return self._verification_token

    @verification_token.setter
    def verification_token(self, verification_token: str) -> None:
        """
            sets the verification token
            :param verification_token: str
            :return: None
        """
        self._verification_token = verification_token

    @property
    def payments(self) -> list:
        """
            payments relationship property
            :return: list
        """
        return self._payments

    @payments.setter
    def payments(self, payment) -> None:
        """
            add PaymentModel Instance to relationship user instance
        :param payment: paymentModel
        :return:
        """
        self._payments.append(payment)

    @property
    def freelancejobs(self) -> list:
        """
            UserModel relationship to FreelanceJobs
        :return:
        """
        return self._freelancejobs

    @freelancejobs.setter
    def freelancejobs(self, freelance_job) -> None:
        """
            sets Freelancejobs Instance to freelancejobs relationship on user
        :param freelance_job:
        :return:
        """
        self._freelancejobs.append(freelance_job)

    # NOTE ACTIONS
    def compare_password(self, password: str) -> bool:
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
        """
            is_admin property
            if user is admin returns true
            :return: bool
        """
        return self.admin

    def __init__(self, email: str, password: str, names: str, surname: str,
                 cell: str, username: str = None, admin: bool = False, img_link: str = None):

        super(UserModel, self).__init__()
        self.uid = str(uuid.uuid4())
        if isinstance(username, str) and (len(username) > 0):
            self.username = username
        else:
            self.username = email

        self.email = email
        self.password = password
        self.names = names
        self.surname = surname
        self.cell = cell
        self.admin = admin
        if isinstance(img_link, str) and (len(img_link) > 0):
            self.img_link = img_link

    def __repr__(self) -> str:
        return '<User username:{} names: {}, surname : {}, cell: {}, email: {}'.format(self.username, self.names,
                                                                                       self.surname, self.cell,
                                                                                       self.email)

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, value) -> bool:
        if value is None:
            return False
        if (self.uid == value.uid) or (self.username == value.username) or (self.email == value.email):
            return True
        return False

    def __bool__(self):
        return False if self.uid is None else True

    @classmethod
    def add_freelance_job(cls, uid: str, freelance_job) -> bool:
        try:
            user_instance = UserModel.query.filter_by(_uid=uid).first()
            user_instance.freelancejobs = freelance_job
            db.session.update(user_instance)
            db.session.commit()
            return True
        except OperationalError:
            return False
        except IntegrityError:
            return False
        except DisconnectionError:
            return False

    @classmethod
    def add_payment(cls, uid: str, payment) -> bool:
        try:
            user_instance = UserModel.query.filter_by(_uid=uid).first()
            user_instance.payments = payment
            db.session.update(user_instance)
            db.session.commit()
            return True
        except OperationalError:
            return False
        except IntegrityError:
            return False
        except DisconnectionError:
            return False

    @staticmethod
    def get_user_by_uid(uid: str) -> any:
        try:
            return UserModel.query.filter_by(_uid=uid).first()
        except OperationalError:
            return None
        except IntegrityError:
            return None
        except DisconnectionError:
            return None

    @staticmethod
    def get_user_by_email(email: str) -> any:
        try:
            return UserModel.query.filter_by(_email=email).first()
        except OperationalError:
            return None
        except IntegrityError:
            return None
        except DisconnectionError:
            return None

    @staticmethod
    def verify_email(token: str) -> bool:
        try:
            user_instance = UserModel.query.filter_by(_verification_token=token).first()
            if isinstance(user_instance, UserModel):
                user_instance.email_is_verified = True
                user_instance.time_email_verified = timestamp()
                return True
            return False
        except OperationalError:
            return False
        except IntegrityError:
            return False
        except DisconnectionError:
            return False

    @staticmethod
    def verify_cell(token: str) -> bool:
        user_instance = UserModel.query.filter_by(_cell_verification_token=token).first()
        if isinstance(user_instance, UserModel):
            user_instance.cell_is_verified = True
            user_instance.time_cell_verified = timestamp()
            return True
        return False

    @staticmethod
    def send_email_verification():
        # TODO- Use Flask- to s
        print("Sending email verification")
        pass

    @staticmethod
    def send_cell_verification():
        print("Sending cell verification")
        pass


# SQLAlchemy Events
def on_email_change_event(target, value, oldvalue, initiator):
    if not is_email(value.trim()):
        raise ValueError('Invalid email format')
    if value.trim() != oldvalue:
        # target.email_is_verified = False
        pass
    return value.trim()


def on_cell_change_event(target, value, oldvalue, initiator):
    if not is_cell(value.trim()):
        raise ValueError('Invalid cell number format')
    if value.trim() != oldvalue:
        # target.cell_is_verified = False
        pass
    return value.trim()


def trigger_send_email_verification(target, value, oldvalue, initiator):
    if value:
        # target.send_email_verification()
        pass
    return value


def trigger_send_cell_verification(target, value, oldvalue, initiator):
    if value:
        # target.send_cell_verification()
        pass
    return value


listen(UserModel._email, 'set', on_email_change_event, retval=True)
listen(UserModel._cell, 'set', on_cell_change_event, retval=True)
listen(UserModel._email_is_verified, 'set', trigger_send_email_verification, retval=True)
listen(UserModel._cell_is_verified, 'set', trigger_send_cell_verification, retval=True)
# TODO- consider adding a UserModel Listener for new user that will look if there is a contact message in contacts
#  and add those messages if there are any

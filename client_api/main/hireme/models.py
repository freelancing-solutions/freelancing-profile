from sqlalchemy.exc import OperationalError
from .. import db
from sqlalchemy.event import listen
from ..library.utils import timestamp, const
import uuid


# noinspection DuplicatedCode,PyArgumentList
class FreelanceJobModel(db.Model):
    """
        id = db.Column(db.Integer, primary_key=True)
        uid = db.Column(db.String(128),unique=True)
        username = db.Column(db.String(128), unique=True, nullable=True)
        Args:
            db ([type]): [description]

        to access payment information use relationship = payment a record
        to access user backref is user
    """
    __bind_key__ = "app"
    _uid = db.Column(db.String(const.uuid_len), db.ForeignKey('user_model._uid'), unique=False, nullable=False)
    _project_id = db.Column(db.String(const.uuid_len), unique=True, primary_key=True)
    _project_name = db.Column(db.String(const.project_name_len), unique=False, nullable=False)
    _project_category = db.Column(db.String(const.project_cat_len), nullable=False, default="webdev")
    # TODO- consider revising description into a TEXT Field
    _description = db.Column(db.String(const.description_len), nullable=False)
    _progress = db.Column(db.Integer, nullable=False, default=0)
    _status = db.Column(db.String(const.project_status_len), nullable=False, default="active")
    _link_details = db.Column(db.String(const.link_len), nullable=False)
    _time_created = db.Column(db.Integer, nullable=False, default=timestamp())
    _est_hours_to_complete = db.Column(db.Integer, nullable=False, default=const.default_project_hours)
    _currency = db.Column(db.String(const.currency_len), nullable=False, default="USD")
    _budget_allocated = db.Column(db.Integer, nullable=False, default=0)
    _total_paid = db.Column(db.Integer, nullable=False, default=0)
    _seen = db.Column(db.Boolean, default=False)
    _payment = db.relationship('PaymentModel', backref=db.backref('freelancejob', lazy=True), uselist=False)
    _messages = db.relationship('ProjectMessages', backref=db.backref('freelancejob', lazy=True, uselist=True))

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, uid: str) -> None:
        """
        [summary] uid is a user id based on uuid.uuidv4() function
        @property: uid str
        Args:
            uid ([str]): [description]

        Raises:
            ValueError: [when uid is null ValueError is raised]
            TypeError: [When uid is not a string ValueError is raised]
            ValueError: [When uid length is not equal to 36 characters then ValueError]
        """
        if uid is None:
            raise ValueError('UID cannot be null')
        if not isinstance(uid, str):
            raise TypeError('UID can only be a string')
        if len(uid) > const.uuid_len:
            raise ValueError('UID should only be uuid.uuidv4() token')
        self._uid = uid

    @property
    def project_id(self) -> str:
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: str) -> None:
        if project_id is None:
            raise ValueError('Project ID cannot be null')
        if not isinstance(project_id, str):
            raise TypeError('Project ID can only be a string')
        if len(project_id) > const.uuid_len:
            raise ValueError('Project ID should only be uuid.uuidv4() token')
        self._project_id = project_id

    @property
    def project_name(self) -> str:
        return self._project_name

    @project_name.setter
    def project_name(self, project_name: str) -> None:
        if project_name is None:
            raise ValueError('Project Name cannot be null')
        if not isinstance(project_name, str):
            raise TypeError('Project Name can only be a string')

        self._project_name = project_name

    @property
    def project_category(self) -> str:
        return self._project_category

    @project_category.setter
    def project_category(self, project_category: str) -> None:
        if project_category not in ['webdev', 'apidev', 'webapp']:
            raise ValueError('Unknown freelance job category')
        self._project_category = project_category

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        if description is None:
            raise ValueError('Description cannot be null')

        if not isinstance(description, str):
            raise TypeError('Description can only be a str')

        self._description = description

    @property
    def progress(self) -> int:
        return self._progress

    @progress.setter
    def progress(self, progress: int) -> None:
        if not isinstance(progress, int):
            raise TypeError('Progress can only be an integer')

        if 0 <= progress <= 100:
            raise ValueError('Progress out of bounds can only be between 0 and 100')

        self._progress = progress

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        if status not in ['active', 'pending', 'in-progress', 'completed', 'suspended']:
            raise ValueError('Status unknown')
        self._status = status

    @property
    def link_details(self) -> str:
        return self._link_details

    @link_details.setter
    def link_details(self, link_details: str) -> None:
        if link_details is None:
            raise ValueError('Freelance Job SEO Link cannot be Null')
        if not isinstance(link_details, str):
            raise TypeError('Freelance Job Link can only be a String')

        self._link_details = link_details

    @property
    def time_created(self) -> int:
        return self._time_created

    @time_created.setter
    def time_created(self, time_created: int) -> None:

        if time_created is None:
            raise ValueError('Time Created can not be Null')

        if not isinstance(time_created, int):
            raise TypeError('Time created can only be an integer')

        # time created is less than right now this has to be invalid, it has to be a little higher
        if 0 > time_created > timestamp() + 5:
            raise ValueError('Invalid time')

        self._time_created = time_created

    @property
    def est_hours_to_complete(self) -> int:
        return self._est_hours_to_complete

    @est_hours_to_complete.setter
    def est_hours_to_complete(self, est_hours_to_complete: int) -> None:
        if est_hours_to_complete is None:
            raise ValueError('Estimated Hours to Completion cannot be Null')

        if not isinstance(est_hours_to_complete, int):
            raise TypeError('Estimate hours to Completion can only be an integer')

        self._est_hours_to_complete = est_hours_to_complete

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, currency: str) -> None:
        if currency is None:
            raise ValueError('Currency cannot be Null')

        if currency not in const.currency_list:
            raise ValueError('That currency is not supported')

        self._currency = currency

    @property
    def budget_allocated(self) -> int:
        return self._budget_allocated

    @budget_allocated.setter
    def budget_allocated(self, budget_allocated: int) -> None:
        if budget_allocated is None:
            raise ValueError('Budget allocated cannot be Null')
        if not isinstance(budget_allocated, int):
            raise TypeError('Budget Allocated is not an Integer')

        self._budget_allocated = budget_allocated

    @property
    def total_paid(self) -> int:
        return self._total_paid

    @total_paid.setter
    def total_paid(self, total_paid: int) -> None:
        if total_paid is None:
            raise ValueError('Total Paid is not None')

        if not isinstance(total_paid, int):
            raise TypeError

    @property
    def seen(self) -> bool:
        return self._seen

    @seen.setter
    def seen(self, seen: bool) -> None:
        if not isinstance(seen, bool):
            raise TypeError('Seen can only be a boolean')
        self._seen = seen

    # noinspection PyTypeChecker
    @property
    def messages(self) -> list:
        return self._messages

    @messages.setter
    def messages(self, message) -> None:
        if not isinstance(message, ProjectMessages):
            raise TypeError('Message is not an instance of project Messages')
        # This syntax maybe correct
        self._messages.append(message)

    @property
    def payment(self):
        return self._payment

    @payment.setter
    def payment(self, payment):
        self._payment = payment

    def __init__(self, uid: str, project_name: str, description: str, est_hours_to_complete: int, currency: str,
                 budget_allocated: int, project_category: str = "webdev"):
        self.uid = uid
        self.project_id = str(uuid.uuid4())
        self.project_name = project_name
        self.description = description
        self.est_hours_to_complete = est_hours_to_complete
        self.currency = currency
        self.budget_allocated = budget_allocated
        self.project_category = project_category
        self.link_details = str(self.create_link_detail(name=project_name, cat=project_category))
        super(FreelanceJobModel, self).__init__()

    @staticmethod
    def create_link_detail(name: str, cat: str) -> str:
        cat_link = ""
        for cat in cat.split(" "):
            cat_link += cat
        name_link = ""
        for name in name.split(" "):
            name_link += name

        return "/{}/{}".format(cat_link, name_link)

    def __repr__(self) -> str:
        return "<FreelanceJobModel project_name: {}, project_category: {}, description: {}, progress: {}, " \
               "status: {},link_details: {}, time_created: {}, est_hours_to_complete: {}, currency: {}, " \
               "budget_allocated: {}, total_paid: {} >" \
            .format(self.project_name, self.project_category, self.description, self.progress, self.status,
                    self.link_details, self.time_created, self.est_hours_to_complete, self.currency,
                    self.budget_allocated, self.total_paid)

    def __eq__(self, value) -> bool:
        """
            :type value:self
        """
        if (value.uid == self.uid) and (value.project_id == self.project_id) and (
                value.project_name == self.project_name) and (value.project_category == self.project_category):
            return True
        return False

    def __bool__(self):
        return False if self.uid is None else True

    def add_payment(self, payment) -> bool:
        """
            payment must be fully initialized
        :param payment:
        :return:
        """
        try:
            self.payment = payment
            return True
        except OperationalError as e:
            return False

    def add_message(self, message) -> bool:
        """
            message must be fully initialized
        :param message:
        :return:
        """
        try:
            self.messages = message
            return True
        except OperationalError as e:
            return False


# SQLAlchemy Events listeners

class ProjectMessages(db.Model):
    __bind_key__ = "app"
    _message_id = db.Column(db.String(const.uuid_len), primary_key=True, unique=True)
    _uid = db.Column(db.String(const.uuid_len), db.ForeignKey('user_model._uid'), unique=False, nullable=False)
    _project_id = db.Column(db.String(const.uuid_len), db.ForeignKey('freelance_job_model._project_id'), unique=False,
                            nullable=False)
    _time_created = db.Column(db.Integer, nullable=False, default=timestamp())
    _message = db.Column(db.String(const.body_len), nullable=False, unique=False)

    @property
    def uid(self) -> str:
        """
            returns user id of the user who created the message
            :return: str: uid
        """
        return self._uid

    @uid.setter
    def uid(self, uid: str) -> None:
        if uid is None:
            raise ValueError('UID cannot be Null')

        if not isinstance(uid, str):
            raise TypeError('UID can only be a string')
        self._uid = uid

    @property
    def project_id(self) -> str:
        return self._project_id

    @project_id.setter
    def project_id(self, project_id: str) -> None:
        """
        :param project_id:
        :return:
        """
        if project_id is None:
            raise ValueError('Project Id cannot be Null')

        if not isinstance(project_id, str):
            raise TypeError('project Id cannot be Null')
        self._project_id = project_id

    @property
    def time_created(self) -> int:
        """
        :return: int: time_created
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created: int) -> None:
        """
            set time_created
            :param time_created: int
            :return: None
        """
        if time_created is None:
            raise ValueError('time created cannot be Null')
        if not isinstance(time_created, int):
            raise TypeError('time created can only be an int')

        self._time_created = time_created

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, message: str) -> None:
        if message is None:
            raise ValueError(' Message cannot be Null')
        if not isinstance(message, str):
            raise TypeError('Message can only be a string')
        self._message = message

    @property
    def message_id(self) -> str:
        return self._message_id

    @message_id.setter
    def message_id(self, message_id: str) -> None:
        if message_id is None:
            raise ValueError('Message Id cannot be Null')
        if not isinstance(message_id, str):
            raise TypeError('Message Id can only be a string')
        self._message_id = message_id

    def __init__(self, uid, project_id, message):
        super(ProjectMessages, self).__init__()
        self.message_id = str(uuid.uuid4())
        self.uid = uid
        self.project_id = project_id
        self.message = message
        self.time_created = timestamp()

    def __str__(self) -> str:
        return '<Message : {}'.format(self.message)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, value) -> bool:
        if (value.message_id == self.message_id) and (self.message == value.message):
            return True
        return False


def total_paid_updated(target, value, oldvalue, initiator):
    """
        when total_paid gets updated check if the amount is equal to the budget if this is the case
        then create a notification indicating the project is fully paid
    :param target:
    :param value:
    :param oldvalue:
    :param initiator:
    :return:
    """
    print("Target : {}".format(target))
    print("value : {}".format(value))
    # print("old value: {}".format(oldvalue))
    print("initiator : {}".format(initiator))
    return value


listen(FreelanceJobModel._total_paid, 'set', total_paid_updated, retval=True)

# TODO  complete the listeners

# TODO Add UpWork Intergrations to HireMe We need to Support UPWork Contracts and Escrow Payments
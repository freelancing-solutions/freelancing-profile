from .. import db
from flask import current_app,escape
import time, uuid
class FreelanceJobModel(db.Model):
    """
        id = db.Column(db.Integer, primary_key=True)
        uid = db.Column(db.String(128),unique=True)
        username = db.Column(db.String(128), unique=True, nullable=True)
        Args:
            db ([type]): [description]
    """
    _uid = db.Column(db.String(36),db.ForeignKey('user_model._uid'),unique=False, nullable=False)
    _project_id = db.Column(db.String(36), unique=True, primary_key=True)
    _project_name = db.Column(db.String(1048), unique=False, nullable=False)
    _project_category = db.Column(db.String(64), nullable=False, default="webdev")
    _description = db.Column(db.String(2096), nullable=False)
    _progress = db.Column(db.Integer, nullable=False, default=0)
    _status = db.Column(db.String(32), nullable=False, default="active")
    _link_details = db.Column(db.String(256), nullable=False)
    _time_created = db.Column(db.Integer, nullable=False,default=int(float(time.time()) * 1000))
    _est_hours_to_complete = db.Column(db.Integer, nullable=False, default=7*24)
    _currency = db.Column(db.String(32), nullable=False, default="$")
    _budget_allocated = db.Column(db.Integer, nullable=False)
    _total_paid = db.Column(db.Integer, nullable=False, default=0)
    _seen = db.Column(db.Boolean, default=False)
    _user = db.relationship('UserModel', backref=db.backref('freelancejobs', lazy=True))


    @property
    def uid (self) -> str:
        return self._uid

    @uid.setter
    def uid(self,uid):
        if uid is None:
            raise ValueError('UID cannot be null')
        if not isinstance(uid, str):
            raise TypeError('UID can only be a string')
        if len(uid) > 36:
            raise ValueError('UID should only be uuid.uuidv4() token')
        self._uid = uid

    @property
    def project_id(self) -> str:
        return self._project_id

    @project_id.setter
    def project_id(self,project_id):
        if project_id is None:
            raise ValueError('Project ID cannot be null')
        if not isinstance(project_id, str):
            raise TypeError('Project ID can only be a string')
        if len(project_id) > 36:
            raise ValueError('Project ID should only be uuid.uuidv4() token')
        self._project_id = project_id

    @property
    def project_name(self) -> str:
        return self._project_name

    @project_name.setter
    def project_name(self,project_name):
        if project_name is None:
            raise ValueError('Project Name cannot be null')
        if not isinstance(project_name, str):
            raise TypeError('Project Name can only be a string')

        self._project_name = escape(project_name)

    @property
    def project_category(self) -> str:
        return self._project_category

    @project_category.setter
    def project_category(self,project_category):
        if project_category not in ['webdev','apidev','webapp']:
            raise ValueError('Unknown freelance job category')
        self._project_category = project_category

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self,description):
        if description is None:
            raise ValueError('Description cannot be null')

        if not isinstance(description, str):
            raise TypeError('Description can only be a str')

        self._description = escape(description)

    @property
    def progress(self) -> int:
        return self._progress

    @progress.setter
    def progress(self,progress):
        if not isinstance(progress, int):
            raise TypeError('Progress can only be an integer')

        if 0 <= progress <= 100:
            raise ValueError('Progress out of bounds can only be between 0 and 100')

        self._progress = progress

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self,status):
        if status not in ['active','pending','in-progress','completed','suspended']:
            raise ValueError('Status unknown')
        self._status = status

    @property
    def link_details(self) -> str:
        return self._link_details

    @link_details.setter
    def link_details(self,link_details):
        if link_details is None:
            raise ValueError('Freelance Job SEO Link cannot be Null')
        if not isinstance(link_details,str):
            raise TypeError('Freelance Job Link can only be a str')

        self._link_details = link_details

    @property
    def time_created(self) -> int:
        return self._time_created

    @time_created.setter
    def time_created(self,time_created):
        assert(time_created)
        if time_created is None:
            raise ValueError('Time Created can not be Null')

        if not isinstance(time_created,int):
            raise TypeError('Time created can only be an integer')

        self._time_created = time_created


    @property
    def est_hours_to_complete(self) -> int:
        return self._est_hours_to_complete

    @est_hours_to_complete.setter
    def est_hours_to_complete(self,est_hours_to_complete):
        if est_hours_to_complete is None:
            raise ValueError('Estimated Hours to Completion cannot be Null')

        if not isinstance(est_hours_to_complete,int):
            raise TypeError('Estimate hours to Completion can only be an integer')

        self._est_hours_to_complete = est_hours_to_complete

    @property
    def currency (self) -> str:
        return self._currency

    @currency.setter
    def currency(self,currency):
        if currency is None:
            raise ValueError('Currency cannot be Null')

        if currency in ['$', "R"]:
            raise ValueError('That currency is not supported')

        self._currency = currency

    @property
    def budget_allocated(self) -> int:
        return self._budget_allocated

    @budget_allocated.setter
    def budget_allocated(self,budget_allocated):
        if budget_allocated is None:
            raise ValueError('Budget allocated cannot be Null')
        if not isinstance(budget_allocated,int):
            raise TypeError('Budget Allocated is not an Integer')

        self._budget_allocated = budget_allocated

    @property
    def total_paid(self):
        return self._total_paid

    @total_paid.setter
    def total_paid(self,total_paid):
        if total_paid is None:
            raise ValueError('Total Paid is not None')

        if not isinstance(total_paid, int):
            raise TypeError

    @property
    def seen(self) -> bool:
        return self._seen

    @seen.setter
    def seen(self,seen):
        if not isinstance(seen,bool):
            raise TypeError('Seen can only be a boolean')
        self._seen = seen



    def __init__(self,uid,project_name,description,est_hours_to_complete,currency,budget_allocated,project_category="webdev"):
        self.uid = uid
        self.project_id = uuid.uuid4()
        self.project_name = project_name
        self.description = description
        self.est_hours_to_complete = est_hours_to_complete
        self.currency = currency
        self.budget_allocated = budget_allocated
        self.link_details = self.create_link_detail(name=project_name,cat=project_category)
        super(FreelanceJobModel).__init__()

    @staticmethod
    def create_link_detail(name,cat):

        cat_link = ""
        for cat in cat.split(" "):
            cat_link += cat
        name_link = ""
        for name in name.split(" "):
            name_link += name

        return "/{}/{}".format(cat_link,name_link).encode("UTF-8")

    def __repr__(self):
        return "<FreelanceJobModel project_name: {}, project_category: {}, description: {}, progress: {}, status: {},\
            link_details: {}, time_created: {}, est_hours_to_complete: {}, currency: {}. budget_allocated: {}, total_paid: {} >".format(
            self.project_name, self.project_category, self.description, self.progress, self.status, self.link_details,
            self.time_created, self.est_hours_to_complete, self.currency, self.budget_allocated, self.total_paid)

    def __eq__(self, value):
        if (value.uid == self.uid) and (value.project_id == self.project_id) and (value.project_name == self.project_name) and (value.project_category == self.project_category) and (value.description == self.description) and (value.progress == self.progress) and (value.status == self.status) and (value.link_details == self.link_details) and (value.time_created == self.time_created) and (value.est_hours_to_complete == self.est_hours_to_complete) and (value.currency == self.currency) and (value.budget_allocated == self.budget_allocated) and (value.total_paid == self.total_paid):
            return True
        return False




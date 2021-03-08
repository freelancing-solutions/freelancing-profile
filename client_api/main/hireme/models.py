from .. import db
from flask import current_app
import time, uuid
class FreelanceJobModel(db.Model):
    """
        id = db.Column(db.Integer, primary_key=True)
        uid = db.Column(db.String(128),unique=True)
        username = db.Column(db.String(128), unique=True, nullable=True)
        Args:
            db ([type]): [description]
    """
    uid = db.Column(db.String(36),db.ForeignKey('user_model.uid'),unique=False, nullable=False)
    project_id = db.Column(db.String(36), unique=True, primary_key=True)
    project_name = db.Column(db.String(1048), unique=False, nullable=False)
    project_category = db.Column(db.String(64), nullable=False, default="webdev")
    description = db.Column(db.String(2096), nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(32), nullable=False, default="active")
    link_details = db.Column(db.String(256), nullable=False)
    time_created = db.Column(db.Integer, nullable=False,default=int(float(time.time()) * 1000))
    est_hours_to_complete = db.Column(db.Integer, nullable=False, default=7*24)
    currency = db.Column(db.String(32), nullable=False, default="$")
    budget_allocated = db.Column(db.Integer, nullable=False)
    total_paid = db.Column(db.Integer, nullable=False, default=0)
    seen = db.Column(db.Boolean, default=False)
    user = db.relationship('UserModel', backref=db.backref('freelancejobs', lazy=True))

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


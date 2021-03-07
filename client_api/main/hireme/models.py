from .. import db
from flask import current_app
import time
class FreelanceJobModel(db.Model):
    """
        id = db.Column(db.Integer, primary_key=True)
        uid = db.Column(db.String(128),unique=True)
        username = db.Column(db.String(128), unique=True, nullable=True)
        Args:
            db ([type]): [description]
    """
    uid = db.Column(db.String(128),db.ForeignKey('user_model.uid'),unique=False, nullable=False)
    project_id = db.Column(db.Integer, unique=True, primary_key=True)
    project_name = db.Column(db.String(1048), unique=False, nullable=False)
    project_category = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(2096), nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(32), nullable=False, default="active")
    link_details = db.Column(db.String(256), nullable=False)
    time_created = db.Column(db.Integer, nullable=False,default=int(float(time.time()) * 1000))
    est_hours_to_complete = db.Column(db.Integer, nullable=False, default=7*24)
    currency = db.Column(db.String(32), nullable=False, default="$")
    budget_allocated = db.Column(db.Integer, nullable=False)
    total_paid = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship('UserModel', backref=db.backref('freelancejobs', lazy=True))

    def __repr__(self):
        return "<FreelanceJobModel project_name: {}, project_category: {}, description: {}, progress: {}, status: {},\
            link_details: {}, time_created: {}, est_hours_to_complete: {}, currency: {}. budget_allocated: {}, total_paid: {} >".format(
            self.project_name, self.project_category, self.description, self.progress, self.status, self.link_details,
            self.time_created, self.est_hours_to_complete, self.currency, self.budget_allocated, self.total_paid)

    def __eq__(self, value):
        if (value.uid == self.uid) and (value.project_id == self.project_id) and (value.project_name == self.project_name) and (value.project_category == self.project_category) and (value.description == self.description) and (value.progress == self.progress) and (value.status == self.status) and (value.link_details == self.link_details) and (value.time_created == self.time_created) and (value.est_hours_to_complete == self.est_hours_to_complete) and (value.currency == self.currency) and (value.budget_allocated == self.budget_allocated) and (value.total_paid == self.total_paid):
            return True
        return False


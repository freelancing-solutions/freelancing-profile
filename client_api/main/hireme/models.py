from .. import db
from flask import current_app

class FreelanceJobModel(db.Model):
    """
        'uid': '546034t045t0459t45', # user id of the user who created the project
        'project_id': '02349u3rf3945394yr7',
        'project_name': 'Web Development',
        'project_category': 'Web Development',
        'description': 'Create a business presence website for my poultry farms it must allow order taking onsite',
        'progress': 70,
        'status': 'in-progress',
        'link_details': '02349u3rf3945394yr7',
        'time_created': time.time() * 1000, # time in milliseconds
        'est_hours_to_complete':0,   # time in milliseconds left until project is completed
        'currency' : '$',
        'budget_allocated': 500,
        'total_paid': 200

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(128),unique=True)
    username = db.Column(db.String(128), unique=True, nullable=True)
    Args:
        db ([type]): [description]
    """
    uid = db.Column(db.String(128),unique=False, nullable=False)
    project_id = db.Column(db.Integer, unique=True, primary_key=True)
    project_name = db.Column(db.String(1048), unique=False, nullable=False)
    project_category = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(2096), nullable=False)
    progress = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(32), nullable=False)
    link_details = db.Column(db.String(256), nullable=False)
    time_created = db.Column(db.Integer, nullable=False)
    est_hours_to_complete = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(32), nullable=False)
    budget_allocated = db.Column(db.Integer, nullable=False)
    total_paid = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return "<FreelanceJobModel project_name: {}, project_category: {}, description: {}, progress: {}, status: {},\
            link_details: {}, time_created: {}, est_hours_to_complete: {}, currency: {}. budget_allocated: {}, total_paid: {} >".format(
            self.project_name, self.project_category, self.description, self.progress, self.status, self.link_details,
            self.time_created, self.est_hours_to_complete, self.currency, self.budget_allocated, self.total_paid)

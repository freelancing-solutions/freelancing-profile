# import unittest
import uuid, time
from .. import db, create_app
from flask import current_app


    # uid = db.Column(db.String(128),unique=False, nullable=False)
    # project_id = db.Column(db.Integer, unique=True, primary_key=True)
    # project_name = db.Column(db.String(1048), unique=False, nullable=False)
    # project_category = db.Column(db.String(64), nullable=False)
    # description = db.Column(db.String(2096), nullable=False)
    # progress = db.Column(db.Integer, nullable=False)
    # status = db.Column(db.String(32), nullable=False)
    # link_details = db.Column(db.String(256), nullable=False)
    # time_created = db.Column(db.Integer, nullable=False)
    # est_hours_to_complete = db.Column(db.Integer, nullable=False)
    # currency = db.Column(db.String(32), nullable=False)
    # budget_allocated = db.Column(db.Integer, nullable=False)
    # total_paid = db.Column(db.Integer, nullable=False)

def test_blog_routes():
    from ..blog import routes
    pass

def test_hireme_routes():
    from ..hireme import routes
    pass

def test_hireme_freelance_job_model():
    from ..hireme.models import FreelanceJobModel
    uid = str(uuid.uuid4())
    project_name = "Website Development"
    project_category = "Website"
    description = "Develop my website/blog based on wordpress"
    progress = 24
    status = "started"
    link_details = "/website/website-development"
    hours_to_complete = 24 * 7
    right_now_milliseconds = int(float(time.time()) * 1000)
    currency = "R"
    budget_allocated = 520
    total_paid = 100
    freelance_job_model = FreelanceJobModel(uid=uid,project_name=project_name,project_category=project_category,
    description=description,progress=progress,status=status,link_details=link_details,time_created=right_now_milliseconds,
    est_hours_to_complete=hours_to_complete,currency=currency,budget_allocated=budget_allocated,total_paid=total_paid)

    assert isinstance(freelance_job_model,FreelanceJobModel), "Failed to created an instance of freelance model"
    assert freelance_job_model.budget_allocated == budget_allocated , "Failed to set budget_allocated"
    assert freelance_job_model.project_name == project_name , "Project Name set incorrectly"
    assert freelance_job_model.description == description, "Failed to set description"
    assert freelance_job_model.progress == progress, "Failed to set progress indicator"
    assert freelance_job_model.status == status, "Failed to set status"
    assert freelance_job_model.link_details == link_details, "Failed to set link_details"
    assert freelance_job_model.est_hours_to_complete == hours_to_complete, "Failed to set hours to complete"
    assert freelance_job_model.time_created == right_now_milliseconds, "Failed to set time created"
    assert freelance_job_model.currency == currency, "Failed to set currency"
    assert freelance_job_model.budget_allocated == budget_allocated, "Failed to set budget allocated"
    assert freelance_job_model.total_paid == total_paid, "Failed to set total paid"

    app = create_app()
    app.app_context().push()
    with app.app_context():
        db.session.add(freelance_job_model)
        db.session.flush()
        db.session.commit()

        freelance_job_mo = FreelanceJobModel.query.filter_by(uid=uid).first()

    assert freelance_job_mo == freelance_job_model, "Instance Values from database are not equal to created instances"






# import unittest
import uuid, time
from .. import db, create_app
from flask import current_app
from ..library import config

def test_hireme_freelance_job_model():
    from ..hireme.models import FreelanceJobModel
    from ..users.models import UserModel
    if not current_app:
        app = create_app(config_class=config.TestingConfig)
        app.app_context().push()
    else:
        app = current_app
    app.testing = True
    with app.app_context():
        user_model_list = UserModel.query.limit(1).all()
        if len(user_model_list) > 0:
            user_instance = user_model_list[0]
            uid = user_instance.uid
        else:
            uid = ""
            assert False, "Could not retrieve user detail test failed"

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
        print("Testing hireme freelance jobs models")
        assert isinstance(freelance_job_model,FreelanceJobModel), "Failed to created an instance of freelance model"
        print("freelance job models are created correctly")
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

        try:
            db.session.add(freelance_job_model)
            db.session.flush()
            db.session.commit()
        except Exception as error:
            assert False, "Could not save freelance model to database"

        freelance_job_mo = FreelanceJobModel.query.filter_by(uid=uid).first()
        assert freelance_job_mo, "Cannot retrieve freelance job model from database"
        assert freelance_job_mo == freelance_job_model, "Instance Values from database are not equal to created instances"

        db.session.delete(freelance_job_model)
        db.session.flush()
        db.session.commit()

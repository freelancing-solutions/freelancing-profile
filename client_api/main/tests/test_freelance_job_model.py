# import unittest
import uuid, time

from sqlalchemy.exc import OperationalError

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
        project_category = "webdev"
        description = "Develop my website/blog based on wordpress"
        hours_to_complete = 24 * 7
        currency = "R"
        budget_allocated = 520
        freelance_job_model = FreelanceJobModel(uid=uid,project_name=project_name,project_category=project_category,
        description=description,est_hours_to_complete=hours_to_complete,currency=currency,budget_allocated=budget_allocated)
        print("Testing hireme freelance jobs models")
        assert isinstance(freelance_job_model,FreelanceJobModel), "Failed to created an instance of freelance model"
        print("freelance job models are created correctly")
        assert freelance_job_model.budget_allocated == budget_allocated , "Failed to set budget_allocated"
        assert freelance_job_model.project_name == project_name , "Project Name set incorrectly"
        assert freelance_job_model.description == description, "Failed to set description"
        assert freelance_job_model.est_hours_to_complete == hours_to_complete, "Failed to set hours to complete"
        assert freelance_job_model.currency == currency, "Failed to set currency"
        assert freelance_job_model.budget_allocated == budget_allocated, "Failed to set budget allocated"

        try:
            db.session.add(freelance_job_model)
            db.session.flush()
            db.session.commit()
        except OperationalError as error:
            assert False, "Could not save freelance model to database"

        freelance_job_mo = FreelanceJobModel.query.filter_by(_uid=uid).first()
        assert freelance_job_mo, "Cannot retrieve freelance job model from database"
        assert freelance_job_mo == freelance_job_model, "Instance Values from database are not equal to created instances"

        db.session.delete(freelance_job_model)
        db.session.flush()
        db.session.commit()

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


def test_main_contact_model():
    from ..main.models import ContactModel


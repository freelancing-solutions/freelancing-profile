# import unittest
import uuid, time
from .. import db, create_app
from flask import current_app

def test_main_contact_model():
    from ..main.models import ContactModel
    uid = uuid.uuid4()
    names = "justice"
    email = "mobius-{}@gmail.com".format(uid)
    cell = "0734562789"
    subject = "This is a test message"
    body="This is a test message"
    reason="test"
    contact_model_instance = ContactModel(uid=uid,names=names,email=email,cell=cell,subject=subject,body=body,reason=reason)

    assert contact_model_instance.uid == uid, "UID is not being set correctly"
    assert contact_model_instance.names == names, "Names is not being set correctly"
    assert contact_model_instance.email == email, "Email is not being set correctly"
    assert contact_model_instance.cell == cell, "Cell is not being set correctly"
    assert contact_model_instance.subject == subject, "Subject is not being set correctly"
    assert contact_model_instance.body == body, "Body is not being set correctly"
    assert contact_model_instance.reason == reason, "Reason is not being set correctly"

    if not current_app:
        app = create_app()
        app.app_context().push()
    else:
        app = current_app

    with app.app_context():
        try:
            db.session.add(contact_model_instance)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            db.session.commit()
            assert False, "Failed to add contact model to database"

        contact_model_data = ContactModel.query.filter_by(uid=uid).first()

        assert contact_model_data, "Contact model is not being retrieved from database"
        assert contact_model_data == contact_model_instance, "Contact Model from database isnt equal to the model stored"






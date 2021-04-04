import uuid, time

from pymysql import IntegrityError
from sqlalchemy.exc import OperationalError
import random

from .. import db, create_app
from flask import current_app
from ..library import config


def test_payments_model():
    from ..payments.models import PaymentModel, TransactionModel
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

        project_models_list = FreelanceJobModel.query.all()
        if len(project_models_list) > 0:
            project_instance = random.choice(project_models_list)
            project_id = project_instance.project_id
        else:
            project_id = ""
            assert False, "Could not locate any project"
        budget = 1500
        currency = "usd"
        payment_instance = PaymentModel(uid=uid, project_id=project_id,
                                        amount=budget, currency=currency)
        assert payment_instance.uid == uid, "UID not set correctly"
        assert payment_instance.project_id == project_id, "Project ID not set correctly"
        assert payment_instance.amount == budget, "Budget not set correctly"
        assert payment_instance.currency == currency, "Currency not set correctly"
        budget = 5000
        currency = "USD"
        payment_instance = PaymentModel(uid=uid, project_id=project_id,
                                        amount=budget, currency=currency)
        try:
            db.session.add(payment_instance)
            db.session.flush()
            db.session.commit()

        except OperationalError as e:
            db.session.rollback()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            db.session.commit()

        payment_instance = PaymentModel.query.filter_by(_payment_id=payment_instance.payment_id).first()

        assert isinstance(payment_instance.last_transaction_date, int), "Last transaction date should be integer"
        assert isinstance(payment_instance.transactions, list), "Transactions should be list"
        assert isinstance(payment_instance.balance, int), "Balance should be integer"
        assert isinstance(payment_instance.total_paid, int), "Total Paid should be Integer"
        assert isinstance(payment_instance.amount, int), "Amount should be integer"

        assert payment_instance.amount == budget, "Budget not set correctly"
        assert payment_instance.currency == currency, "Currency not set correctly"
        assert payment_instance.total_paid == 0, "Total paid not set correctly"
        assert payment_instance.balance == budget, "Balance not set correctly"

        assert payment_instance.last_transaction_date == 0, "Last Transaction not set correctly"
        assert payment_instance.is_fully_paid == False, "Is Fully not set correctly"
        assert payment_instance.time_created > 0, "Time created paid not set correctly"
        db.session.rollback()
        db.session.commit()



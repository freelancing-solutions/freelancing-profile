

def add_admin_user(app):
    from sqlalchemy.exc import OperationalError, DisconnectionError, IntegrityError
    from main import db
    from main.users.models import UserModel
    try:

        user_details = app.config['ADMIN_USER']
        try:
            user_instance = UserModel.query.filter_by(_email=user_details['EMAIL']).first()
        except OperationalError as e:
            user_instance = None

        if not(user_instance and user_instance.uid):
            admin_user = UserModel(names=user_details['NAMES'], surname=user_details['SURNAME'],
                                   username=user_details['USERNAME'], email=user_details['EMAIL'],
                                   password=user_details['PASSWORD'], cell=user_details['CELL'],
                                   admin=user_details['ADMIN'])
            db.session.add(admin_user)
            db.session.commit()

    except OperationalError as e:
        pass
    except IntegrityError as e:
        pass
    except DisconnectionError as e:
        pass


def create_databases(app):
    from sqlalchemy.exc import OperationalError, DisconnectionError, IntegrityError
    from main import db
    try:
        # db.drop_all(app=app)
        db.create_all(app=app)
    except OperationalError as e:
        pass


def setup_sentry(app):
    try:
        # TODO- Properly Implement Logging Support
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        # Sentry based Error Reporting and Logging
        sentry_sdk.init(
            dsn=app.config['SENTRY_INIT'],
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )
    # TODO - Find the specific error to capture here- a great place to check will be at the sentry documentation
    except Exception as e:
        print('sentry error : {}'.format(e))

from flask import current_app
import logging
from logging.handlers import SMTPHandler


class EmailErrorLogger:
    """
        admin email is the email allowed to send mail from the server
    """
    app_admins: list = list()
    admin_email: str = str()
    server_ip: str = '127.0.0.1'
    email_heading: str = str()
    username: str = str()
    password: str = str()
    mail_handler = None

    def __init__(self, app=None, admin_email=None, app_admins=None, server_ip=None):
        super(EmailErrorLogger, self).__init__()
        with app.app_context():
            config = app.config
            self.app_admins = app_admins if app_admins is not None else config.get('APP_ADMINS')
            self.admin_email = admin_email if admin_email is not None else config.get('MAIL_USERNAME')
            self.server_ip = server_ip if server_ip is not None else config.get('MAIL_SERVER')
            self.password = config.get('MAIL_PASSWORD')
            self.username = config.get('MAIL_USERNAME')

            try:
                self.mail_handler = SMTPHandler(mailhost=self.server_ip,
                                                fromaddr=self.admin_email,
                                                toaddrs=self.app_admins,
                                                subject=self.email_heading,
                                                credentials=(self.username, self.password))
                self.mail_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s: %(message)s"))
            except Exception:
                pass

    @staticmethod
    def get_app(reference_app=None):
        """Helper method that implements the logic to look up an
        application."""

        if reference_app is not None:
            return reference_app

        if current_app:
            return current_app._get_current_object()

        raise RuntimeError(
            ' No application found. Either work inside a view function or push '
            ' an application context. See'
            ' http://flask-sqlalchemy.pocoo.org/contexts/.'
        )

    def init_app(self, app, name):
        if self.mail_handler:
            app = self.get_app(reference_app=app)
            app.logger = logging.getLogger(name)
            app.logger.addHandler(self.mail_handler)
            app.logger.setLevel(logging.ERROR)
            return app.logger
        else:
            return None



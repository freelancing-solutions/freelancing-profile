import os
from decouple import config


class Config:
    """
        All Configuration settings for the application will be stored here
    """
    MAIL_SERVER = 'https://gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or config('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or config('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@127.0.0.1:3306/ajfreelance'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or config('SECRET_KEY')
    SENTRY_INIT = os.environ.get('SENTRY_INIT') or config('SENTRY_INIT')
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    TESTING = False
    # Find a way to set Debug to False on production


class ProductionConfig(Config):
    TEMPLATES_AUTO_RELOAD = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or config('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY') or config('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or config('SQLALCHEMY_DATABASE_URI')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or config('SQLALCHEMY_DATABASE_URI')
    SERVER_NAME = os.environ.get('SERVER_NAME')
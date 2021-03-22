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
    SQLALCHEMY_BINDS = {
        "app": os.environ.get("APP_DB_URI") or config("APP_DB_URI"),
        "blog": os.environ.get("BLOG_DB_URI") or config("BLOG_DB_URI")
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or config('SECRET_KEY')
    SENTRY_INIT = os.environ.get('SENTRY_INIT') or config('SENTRY_INIT')
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    TESTING = False
    # Find a way to set Debug to False on production
    INSTALL = os.environ.get('INSTALL') or config('INSTALL')

    BLOGGING_URL_PREFIX = os.environ.get("BLOGGING_URL_PREFIX") or config("BLOGGING_URL_PREFIX")
    BLOGGING_DISQUS_SITENAME = os.environ.get("BLOGGING_DISQUS_SITENAME") or config("BLOGGING_DISQUS_SITENAME")
    BLOGGING_SITEURL = os.environ.get("BLOGGING_SITEURL") or config("BLOGGING_SITEURL")
    BLOGGING_SITENAME = os.environ.get("BLOGGING_SITENAME") or config("BLOGGING_SITENAME")
    BLOGGING_KEYWORDS = os.environ.get("BLOGGING_KEYWORDS") or config("BLOGGING_KEYWORDS")
    FILEUPLOAD_IMG_FOLDER = os.environ.get("FILEUPLOAD_IMG_FOLDER") or config("FILEUPLOAD_IMG_FOLDER")
    FILEUPLOAD_PREFIX = os.environ.get("FILEUPLOAD_PREFIX") or config("FILEUPLOAD_PREFIX")
    FILEUPLOAD_ALLOWED_EXTENSIONS = os.environ.get("FILEUPLOAD_ALLOWED_EXTENSIONS") or config("FILEUPLOAD_ALLOWED_EXTENSIONS")


class ProductionConfig(Config):
    TEMPLATES_AUTO_RELOAD = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or config('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SERVER_NAME = os.environ.get('SERVER_NAME')

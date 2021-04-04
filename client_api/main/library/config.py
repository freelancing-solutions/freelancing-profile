import os
from decouple import config


class Config:
    """
        All Configuration settings for the application will be stored here
    """
    MAIL_SERVER: str = 'https://googlemail.com'
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME') or config('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD') or config('MAIL_PASSWORD')
    SQLALCHEMY_BINDS: dict = {
        "app": os.environ.get("APP_DB_URI") or config("APP_DB_URI"),
        "blog": os.environ.get("BLOG_DB_URI") or config("BLOG_DB_URI"),
        "settings": os.environ.get("SETTINGS_DB_URI") or config("SETTINGS_DB_URI")
    }
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or config('SECRET_KEY')
    SENTRY_INIT: str = os.environ.get('SENTRY_INIT') or config('SENTRY_INIT')
    TEMPLATES_AUTO_RELOAD: bool = True
    DEBUG: bool = True
    TESTING: bool = False
    # Find a way to set Debug to False on production
    INSTALL: bool = os.environ.get('INSTALL') or config('INSTALL')
    BLOGGING_URL_PREFIX: str = os.environ.get("BLOGGING_URL_PREFIX") or config("BLOGGING_URL_PREFIX")
    BLOGGING_DISQUS_SITENAME: str = os.environ.get("BLOGGING_DISQUS_SITENAME") or config("BLOGGING_DISQUS_SITENAME")
    BLOGGING_SITEURL: str = os.environ.get("BLOGGING_SITEURL") or config("BLOGGING_SITEURL")
    BLOGGING_SITENAME: str = os.environ.get("BLOGGING_SITENAME") or config("BLOGGING_SITENAME")
    BLOGGING_KEYWORDS: str = os.environ.get("BLOGGING_KEYWORDS") or config("BLOGGING_KEYWORDS")

    FILEUPLOAD_IMG_FOLDER: str = os.environ.get("FILEUPLOAD_IMG_FOLDER") or config("FILEUPLOAD_IMG_FOLDER")
    FILEUPLOAD_PREFIX: str = os.environ.get("FILEUPLOAD_PREFIX") or config("FILEUPLOAD_PREFIX")
    FILEUPLOAD_ALLOWED_EXTENSIONS: str = os.environ.get("FILEUPLOAD_ALLOWED_EXTENSIONS") or config("FILEUPLOAD_ALLOWED_EXTENSIONS")
    APP_NAME: str = os.environ.get('APP_NAME') or config('APP_NAME')
    APP_ADMINS: list = os.environ.get('APP_ADMINS') or config('APP_ADMINS')

    BLOGGING_SITEMAP: str = os.environ.get("BLOGGING_SITEMAP") or config("BLOGGING_SITEMAP")
    GITHUB_SITEMAP: str = os.environ.get("GITHUB_SITEMAP") or config("GITHUB_SITEMAP")
    CODEPEN_SITEMAP: str = os.environ.get("CODEPEN_SITEMAP") or config("CODEPEN_SITEMAP")


class ProductionConfig(Config):
    TEMPLATES_AUTO_RELOAD: bool = False
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or config('SECRET_KEY')
    SQLALCHEMY_BINDS: dict = {
        "app": os.environ.get("APP_DB_URI") or config("APP_DB_URI"),
        "blog": os.environ.get("BLOG_DB_URI") or config("BLOG_DB_URI"),
        "settings": os.environ.get("SETTINGS_DB_URI") or config("SETTINGS_DB_URI")
    }
    prefix = os.environ.get('APP_NAME') or config('APP_NAME')
    CACHE_CONFIG: dict = {
        "CACHE_TYPE": "simple",
        "CACHE_THRESHOLD": 1024,
        "CACHE_KEY_PREFIX": prefix.replace(" ", "") + "_"
    }

    # TODO- consider adding a redis cache here

    APP_ADMINS: list = os.environ.get('APP_ADMINS') or config('APP_ADMINS')
    # LOAD THIS from config file it needs to be a real ADMIN Account
    ADMIN_USER: dict = {
        "USERNAME": os.environ.get("ADMIN_USERNAME") or config("ADMIN_USERNAME"),
        "EMAIL": os.environ.get("ADMIN_EMAIL") or config("ADMIN_EMAIL"),
        "NAMES": os.environ.get("ADMIN_NAMES") or config("ADMIN_NAMES"),
        "SURNAME": os.environ.get("ADMIN_SURNAME") or config("ADMIN_SURNAME"),
        "CELL": os.environ.get("ADMIN_CELL") or config("ADMIN_CELL"),
        "PASSWORD": os.environ.get("ADMIN_PASSWORD") or config("ADMIN_PASSWORD"),
        "ADMIN": True
    }


class DevelopmentConfig(Config):
    DEBUG: bool = True
    SQLALCHEMY_BINDS: dict = {
        "app": os.environ.get("APP_DB_URI") or config("APP_DB_URI"),
        "blog": os.environ.get("BLOG_DB_URI") or config("BLOG_DB_URI"),
        "settings": os.environ.get("SETTINGS_DB_URI") or config("SETTINGS_DB_URI")
    }
    prefix = os.environ.get('APP_NAME') or config('APP_NAME')
    CACHE_CONFIG: dict = {
        "CACHE_TYPE": "simple",
        "CACHE_THRESHOLD": 1024,
        "CACHE_KEY_PREFIX": prefix.replace(" ", "") + "_"
    }
    ADMIN_USER: dict = {
        "USERNAME": "example@example.com",
        "EMAIL": "example@example.com",
        "NAMES": "mobius",
        "SURNAME": "crypt",
        "CELL": "0712345678",
        "PASSWORD": "123456",
        "ADMIN": True
    }
    APP_ADMINS: list = os.environ.get('APP_ADMINS') or config('APP_ADMINS')
    INSTALL: bool = True


class TestingConfig(Config):
    TESTING: bool = True
    DEBUG: bool = True
    SERVER_NAME: str = os.environ.get('SERVER_NAME')
    prefix = os.environ.get('APP_NAME') or config('APP_NAME')
    CACHE_CONFIG: dict = {
        "CACHE_TYPE": "simple",
        "CACHE_THRESHOLD": 1024,
        "CACHE_KEY_PREFIX": prefix.replace(" ", "") + "_"
    }

import os
class Config:
    """
        All Configuration settings for the application will be stored here
    """
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:11111111@localhost/ajfreelance'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


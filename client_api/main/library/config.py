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
    SECRET_KEY = "\xd6\xcf#\x89K\x1a\xad\xf0\xbec\xce\xf5Gw\xd06\xfd4\x9d\x8bRn]S\xc2a*\xa6\x17l\r\xbf\x8b\x10[y\xb4Pg\xe9[\xdc\xd1\x1c\xca6\x06\t\xa8\x11\x1d\xc7\x8cB\x1c\x0c\xa5\xf63\xcfVB\x88"

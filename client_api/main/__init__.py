
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from client_api.main.rest_api import ContactAPI, Blog, Freelancer, Github, Sitemap
from client_api.main.library.config import Config
api = Api()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    # TODO- Add Extensions here
    # TODO- Add API Resources
    api.init_app(app)

    # importing blue prints
    from client_api.main.blog import blog_bp
    from client_api.main import hireme
    from client_api.main.main.routes import main
    from client_api.main.projects import projects_bp
    from client_api.main.users.routes import users

    app.register_blueprint(blog_bp)
    app.register_blueprint(hireme)
    app.register_blueprint(main)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users)

    return app

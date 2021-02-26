
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from main.rest_api import ContactAPI, Blog, Freelancer, Github, Sitemap
from main.library.config import Config
api = Api()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    # TODO- Add Extensions here
    # TODO- Add API Resources
    api.add_resource(ContactAPI, '/api/v1/contact/<string:uid>', endpoint='get_contact') # Get Method
    api.add_resource(ContactAPI, '/api/v1/contact', endpoint='post_contact') # Post Method
    api.add_resource(ContactAPI, '/api/v1/contacts/<string:contact_id>', endpoint='put_contact',)  # Update Method

    api.init_app(app)

    # importing blue prints
    from main.blog.routes import blog_bp
    from main.hireme.routes import hireme
    from main.main.routes import main
    from main.projects.routes import projects_bp
    from main.users.routes import users

    app.register_blueprint(blog_bp)
    app.register_blueprint(hireme)
    app.register_blueprint(main)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users)

    return app

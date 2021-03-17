
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_restful import Api
from .rest_api import UserAPI, ContactAPI, Blog, FreelanceJobAPI,ListFreelanceJobs, Github, Sitemap
from .library.config import Config
import logging
api = Api()
try:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    # Sentry based Error Reporting and Logging
    sentry_sdk.init(
        dsn=Config().SENTRY_INIT,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )

    # Error Logging
    # Logging configuration
    logging.basicConfig(filename='demo.log', level=logging.DEBUG)

except Exception as e:
    pass


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # TODO- find a way to restructure api
    # NOTE that API are mainly used by admin user
    api.add_resource(ContactAPI, '/api/v1/contact/<string:contact_id>', endpoint='get_contact_details', methods=['GET']) # Get Method
    api.add_resource(ContactAPI, '/api/v1/contact', endpoint='post_contact', methods=['POST']) # Post Method
    api.add_resource(ContactAPI, '/api/v1/contacts/<string:contact_id>', endpoint='put_contact', methods=['PUT'])  # Update Method

    api.add_resource(UserAPI, '/api/v1/users/<string:uid>', endpoint='get_user', methods=['GET']) # 'GET SPECIFIC USER
    api.add_resource(UserAPI, '/api/v1/user', endpoint='create_user', methods=['POST']) #'Create New User

    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-job/<string:project_id>', endpoint="get_freelance_job", methods=['GET']) # Method Get
    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-job', endpoint='create_freelance_job',methods=['POST']) # Method POST Create Freelance Job
    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-jobs/<string:project_id>', endpoint='update_freelance_job',methods=['PUT']) # Method PUT Update Freelance Job
    api.add_resource(ListFreelanceJobs, '/api/v1/freelance-jobs', endpoint="list_freelance_jobs",methods=['GET']) # Method Get use x-access-token header for access

    db.init_app(app)
    api.init_app(app)

    # importing blue prints
    from .users.routes import users
    from .blog.routes import blog_bp
    from .hireme.routes import hireme
    from .main.routes import main
    from .projects.routes import projects_bp
    from .errorhandlers.routes import error_blueprint
    from .administrator.routes import admin_routes

    app.register_blueprint(error_blueprint)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(blog_bp)
    app.register_blueprint(hireme)
    app.register_blueprint(projects_bp)
    app.register_blueprint(admin_routes)
    return app

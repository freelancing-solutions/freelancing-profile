
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_restful import Api
from .rest_api import ContactAPI, Blog, FreelanceJobAPI,ListFreelanceJobs, Github, Sitemap, UserAPI
from .library.config import Config
api = Api()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)


    # TODO- find a way to restructure api
    # NOTE that API are mainly used by admin user
    api.add_resource(ContactAPI, '/api/v1/contact/<string:contact_id>', endpoint='get_contact') # Get Method
    api.add_resource(ContactAPI, '/api/v1/contact', endpoint='post_contact') # Post Method
    api.add_resource(ContactAPI, '/api/v1/contacts/<string:contact_id>', endpoint='put_contact')  # Update Method

    api.add_resource(UserAPI, '/api/v1/users/<string:uid>', endpoint='get') # 'GET SPECIFIC USER
    api.add_resource(UserAPI, '/api/v1/user', endpoint='create_user') #'Create New User

    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-job/<string:project_id>', endpoint="get_freelance_job") # Method Get
    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-job', endpoint='create_freelance_job') # Method POST Create Freelance Job
    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-jobs/<string:project_id>', endpoint='update_freelance_job') # Method PUT Update Freelance Job
    api.add_resource(ListFreelanceJobs, '/api/v1/freelance-jobs', endpoint="list_freelance_jobs") # Method Get use x-access-token header for access

    db.init_app(app)
    api.init_app(app)

    # importing blue prints
    from .blog.routes import blog_bp
    from .hireme.routes import hireme
    from .main.routes import main
    from .projects.routes import projects_bp
    from .users.routes import users

    app.register_blueprint(blog_bp)
    app.register_blueprint(hireme)
    app.register_blueprint(main)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users)

    return app

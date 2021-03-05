
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_restful import Api
from main.rest_api import ContactAPI, Blog, FreelanceJobAPI, Github, Sitemap, UserAPI
from main.library.config import Config
api = Api()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    # TODO- Add Extensions here
    # TODO- Add API Resources
    api.add_resource(ContactAPI, '/api/v1/contact/<string:contact_id>', endpoint='get_contact') # Get Method
    api.add_resource(ContactAPI, '/api/v1/contact', endpoint='post_contact') # Post Method
    api.add_resource(ContactAPI, '/api/v1/contacts/<string:contact_id>', endpoint='put_contact')  # Update Method

    api.add_resource(UserAPI, '/api/v1/users/<string:uid>', endpoint='get') # 'GET SPECIFIC USER
    api.add_resource(UserAPI, '/api/v1/user/login', endpoint='loginuser') #'POST REQUEST --Login User

    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-job/<string:project_id>', endpoint="get_freelance_job") # Method Get
    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-job', endpoint='create_freelance_job') # Method POST Create Freelance Job
    api.add_resource(FreelanceJobAPI, '/api/v1/freelance-jobs/<string:project_id>', endpoint='update_freelance_job') # Method PUT Update Freelance Job

    db.init_app(app)
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

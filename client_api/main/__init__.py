
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_restful import Api
# from .rest_api import UserAPI, ContactAPI, Blog, FreelanceJobAPI,ListFreelanceJobs, Github, Sitemap
from .library.config import Config, ProductionConfig, DevelopmentConfig
from flask_blogging import SQLAStorage
from flask_caching import Cache
from flask_login import LoginManager
from .blog.routes import blogging_engine
api = Api()
cache = Cache()
try:
    # TODO- Properly Implement Logging Support
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


except Exception as e:
    print('sentry error : {}'.format(e))


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    with app.app_context():
        cache.init_app(app=app)
        db.init_app(app)
        storage = SQLAStorage(db=db, bind="blog")
        blogging_engine.init_app(app=app, storage=storage, cache=cache)
        login_manager = LoginManager(app=app)
        from .users.models import UserModel

        @login_manager.user_loader
        @blogging_engine.user_loader
        def load_user(userid):
            return UserModel.get(uid=userid)

    # importing blue prints
    from .users.routes import users
    from .blog.routes import blog_bp
    from .hireme.routes import hireme
    from .main.routes import main
    from .projects.routes import projects_bp
    from .errorhandlers.routes import error_blueprint
    from .administrator.routes import admin_routes
    from .payments.routes import payments_bp

    app.register_blueprint(error_blueprint)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(blog_bp)
    app.register_blueprint(hireme)
    app.register_blueprint(projects_bp)
    app.register_blueprint(admin_routes)
    app.register_blueprint(payments_bp)


    return app

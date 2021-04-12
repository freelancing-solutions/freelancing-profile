from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, DisconnectionError
db = SQLAlchemy()
from .library.config import ProductionConfig, DevelopmentConfig
from flask_caching import Cache
from main.server.loggingHandlers import EmailErrorLogger
from .library.utils import is_development
from main.server.stats import StatsLogger
from utils import setup_sentry, create_databases, add_admin_user
from main.app_settings_store.settingsModels import StatsLoggerModel

cache = Cache()
server_stats_logger = StatsLogger()
default_config = DevelopmentConfig if is_development() else ProductionConfig


def create_app(config_class=default_config):

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    # importing blue prints
    from .users.routes import users
    from .blog.routes import blog_bp
    from .hireme.routes import hireme
    from .main.routes import main
    from .projects.routes import projects_bp
    from .errorhandlers.routes import error_blueprint
    from .administrator.routes import admin_routes
    from .payments.routes import payments_bp
    from .notifications.routes import notifications_bp

    with app.app_context():
        # NOTE: this effectively adds a logging handler to the APP
        # Loggers
        setup_sentry(app=app)
        email_logger_handler = EmailErrorLogger(app=app)
        email_logger_handler.init_app(app=app, name=app.config['APP_NAME'] + "_logger")

        try:
            # cache and databases
            cache.init_app(app=app, config=app.config['CACHE_CONFIG'])
            db.init_app(app)
            # if fresh install install
            if app.config['INSTALL']:
                create_databases(app)
                add_admin_user(app)
        except OperationalError as e:
            pass
        except DisconnectionError as e:
            pass

        # will add before and after request handlers, to add timers to every request, for server stats
        server_stats_logger.init_app(app=app, logger_model=StatsLoggerModel)

        # request handlers
        app.register_blueprint(error_blueprint)
        app.register_blueprint(users)
        app.register_blueprint(main)
        app.register_blueprint(blog_bp)
        app.register_blueprint(hireme)
        app.register_blueprint(projects_bp)
        app.register_blueprint(admin_routes)
        app.register_blueprint(payments_bp)
        app.register_blueprint(notifications_bp)

    return app

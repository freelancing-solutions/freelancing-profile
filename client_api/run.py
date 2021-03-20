import os, logging
from main import create_app, db
from main.library.utils import is_development
from main.library.config import Config, DevelopmentConfig, ProductionConfig

# TODO- properly configure logging
logging.basicConfig(filename='logs.log', level='INFO')

if is_development:
    app = create_app(config_class=DevelopmentConfig)
    is_debug = DevelopmentConfig().DEBUG
    log_message = 'Started in development mode'
    print(log_message)
    logging.info(log_message)
else:
    app = create_app(config_class=ProductionConfig)
    is_debug = ProductionConfig().DEBUG
    log_message = 'Started in production environment'
    print(log_message)
    logging.info(log_message)


app.app_context().push()

if Config().INSTALL:
    try:
        db.drop_all(app=app)
        db.create_all(app=app)
        log_message = 'Created new database - fresh install'
        print(log_message)
        logging.info(log_message)
    except Exception as e:
        log_message = 'DB Error creating fresh database'
        print(log_message)
        logging.info(log_message)

if is_debug:
    from main.users.models import UserModel
    try:
        admin_user = UserModel(names='mobius', surname='crypt', username='example@example.com',
                               email='example@example.com', password='123456', cell='0794071559', admin=True)
        db.session.add(admin_user)
        db.session.commit()
        log_message = 'Created admin User'
        print(log_message)
        logging.info(log_message)
    except Exception as e:
        log_message = 'Admin User already Created'
        print(log_message)
        logging.info(log_message)
else:
    log_message = 'Not in debug mode'
    print(log_message)
    logging.info(log_message)

if __name__ == '__main__':
    app.run(debug=is_debug, use_reloader=is_debug, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

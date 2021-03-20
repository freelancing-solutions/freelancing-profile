import os
from main import create_app, db
from main.library.utils import is_development
from main.library.config import Config, DevelopmentConfig, ProductionConfig

if is_development:
    app = create_app(config_class=DevelopmentConfig)
    is_debug = DevelopmentConfig().DEBUG
else:
    app = create_app(config_class=ProductionConfig)
    is_debug = ProductionConfig().DEBUG

app.app_context().push()

if Config().INSTALL:
    try:
        db.create_all(app=app)
    except Exception as e:
        print('db error: {}'.format(e))

if is_debug:
    from main.users.models import UserModel
    try:
        admin_user = UserModel(names='mobius', surname='crypt', username='example@example.com',
                               email='example@example.com', password='123456', cell='0794071559', admin=True)
        db.session.add(admin_user)
        db.session.commit()
    except Exception as e:
        pass

if __name__ == '__main__':
    app.run(debug=is_debug, use_reloader=is_debug, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

import os
from main import create_app, db
from main.library.config import Config

app = create_app()
app.app_context().push()

if Config().DEBUG:
    db.create_all(app=app)

if __name__ == '__main__':
    app.run(debug=Config().DEBUG, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

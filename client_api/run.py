import os
from main import create_app, db
from main.library.config import Config

app = create_app()
# TODO- find a way to create databases conditionally
# Depending on production flag & command line argument or 
# 
app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

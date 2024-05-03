import os
from main import create_app
app = create_app()
# Create app runs main.__init__()
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['DEBUG'],
            host='127.0.0.1', port=8086)

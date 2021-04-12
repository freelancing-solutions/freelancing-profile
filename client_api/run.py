import os
from main import create_app
app = create_app()
# Create app runs main.__init__()
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['DEBUG'],
            host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

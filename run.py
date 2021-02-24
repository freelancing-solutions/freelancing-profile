import os
from main import create_app

if __name__ == '__main__':
    create_app().run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

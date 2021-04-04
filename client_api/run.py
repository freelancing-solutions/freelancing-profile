import os
from main import create_app
from main.library.utils import is_development
from main.library.config import DevelopmentConfig, ProductionConfig

app = create_app(config_class=DevelopmentConfig) if is_development() else create_app(config_class=ProductionConfig)
# Create app runs main.__init__()
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['DEBUG'], host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

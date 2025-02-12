from flask import Flask
from database import init_db
from routes import ussd_callback
from flask_caching import Cache
from flask_admin import Admin
from models import Parent, Child
from flask_admin.contrib.sqla import ModelView
from flask_swagger_ui import get_swaggerui_blueprint
import logging

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config.from_pyfile('config.py')

# Initialize database
init_db()

# Register the USSD route
app.add_url_rule('/ussd', 'ussd_callback', ussd_callback, methods=['POST'])

# Initialize caching
cache = Cache(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': app.config['REDIS_URL']})

# Initialize Flask-Admin
admin = Admin(app, name='Lady’s Essence', template_mode='bootstrap3')
admin.add_view(ModelView(Parent, init_db()))
admin.add_view(ModelView(Child, init_db()))

# Initialize Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Lady’s Essence"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Logging configuration
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return "END An error occurred. Please try again later.", 500

if __name__ == '__main__':
    app.run(port=5000)
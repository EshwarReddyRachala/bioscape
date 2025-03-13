"""
script: app.py

"""

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from api import home_bp, order_bp, status_bp

app = Flask(__name__)

# Swagger UI setup
SWAGGER_URL = "/swagger"  # URL for accessing Swagger UI
API_DOCS_URL = "/static/swagger.json"  # Path to the API docs JSON

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_DOCS_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(home_bp)
app.register_blueprint(order_bp)
app.register_blueprint(status_bp)

app.run()

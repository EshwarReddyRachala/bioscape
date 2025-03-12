"""
script: app.py

"""

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from api.routes.order_routes import order_bp
from api.routes.status_routes import status_bp
from api.routes.home_routes import home_bp


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Swagger UI setup
    swagger_url = "/swagger"  # URL for accessing Swagger UI
    api_docs_url = "/static/swagger.json"  # Path to the API docs JSON

    swagger_ui_blueprint = get_swaggerui_blueprint(swagger_url, api_docs_url)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=swagger_url)
    app.register_blueprint(home_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(status_bp)

    return app

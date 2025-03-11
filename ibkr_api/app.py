from flask import Flask
from setuptools import setup, find_packages
from ibkr_api.routes.order_routes import order_bp
from ibkr_api.routes.status_routes import status_bp
from ibkr_api.routes.home_routes import home_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")
    app.register_blueprint(status_bp, url_prefix="/api")
    return app

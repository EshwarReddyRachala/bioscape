from flask import Flask
from routes.order_routes import order_bp
from routes.status_routes import status_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(order_bp)
    app.register_blueprint(status_bp)
    return app

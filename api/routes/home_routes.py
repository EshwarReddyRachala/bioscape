"""
script: home_routes.py


"""
from flask import Blueprint, jsonify,  render_template


home_bp = Blueprint('home', __name__)

@home_bp.route("/api/home", methods=["GET"])
def home():
    """
    Render the home page.
    """
    return render_template('index.html')


# Sample API endpoint
@home_bp.route('/api/hello', methods=['GET'])
def hello():
    """
    Return a simple JSON response.
    """
    return jsonify({"message": "Hello, World!"})
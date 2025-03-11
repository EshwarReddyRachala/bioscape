from flask import Blueprint, jsonify

status_bp = Blueprint('status_routes', __name__)

@status_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

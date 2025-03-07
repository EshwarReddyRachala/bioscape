from flask import Blueprint, jsonify

status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/status', methods=['GET'])
def get_status():
    """Return a simple status message indicating that the API is running."""
    return jsonify({'status': 'API is running'})


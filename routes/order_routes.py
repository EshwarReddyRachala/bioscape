from flask import Blueprint, jsonify, request
from ibkr_api.ib_connection import ib_connection
from ibkr_api.ib_api import place_order

order_bp = Blueprint('order_routes', __name__)
ib_api = ib_connection.get_ib_api()

@order_bp.route('/place_order', methods=['POST'])
def handle_order():
    data = request.json
    symbol = data.get('symbol')
    action = data.get('action')
    quantity = data.get('quantity')

    if not symbol or not action or not quantity:
        return jsonify({"error": "Invalid input"}), 400

    result = place_order(symbol, action, quantity, ib_api)
    return jsonify(result)

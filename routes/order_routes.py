from flask import Blueprint, jsonify, request
from ibkr_api import ib_connection, place_order

order_blueprint = Blueprint('orders', __name__)
ib_api = ib_connection.get_ib_api()


@order_blueprint.route('/place_order', methods=['POST'])
def place_order_endpoint():
    data = request.json
    symbol = data.get('symbol')
    action = data.get('action')
    quantity = data.get('quantity')

    if not all([symbol, action, quantity]):
        return jsonify({'error': 'Invalid input'}), 400

    result = place_order(symbol, action, quantity, ib_api)
    return jsonify(result)


""""

This module contains the routes for placing orders using the Interactive Brokers API.

The handle_order function receives a POST request with the order details,
including the symbol, action, and quantity. It extracts the details such as the stock symbol, action (BUY or SELL), 
and quantity. It then calls the place_order function from the ibkr_api.ib_api module to place the order using the 
Interactive Brokers API.

The function returns the result of the place_order function as a JSON response.

"""

from flask import Blueprint, jsonify, request
from ibkr_api.ib_connection import ib_connection
from ibkr_api.ib_api import place_order



order_bp = Blueprint('order_routes', __name__)
ibapi = ib_connection.get_ib_api()

@order_bp.route('/place_order', methods=['POST'])
def handle_order():
    """
    Place an order using the Interactive Brokers API.
    
    """
    data = request.json

    symbol = data.get('symbol')
    action = data.get('action')
    quantity = data.get('quantity')

    if not symbol or not action or not quantity:
        return jsonify({"error": "Invalid input"}), 400

    result = place_order(symbol, action, quantity, ibapi)
    return jsonify(result)
""""

This module contains the routes for placing orders using the Interactive Brokers API.

The handle_order function receives a POST request with the order details,
including the symbol, action, and quantity. It extracts the details such as the stock symbol, action (BUY or SELL), 
and quantity. It then calls the place_order function from the ibkr_api.ib_api module to place the order using the 
Interactive Brokers API.

The function returns the result of the place_order function as a JSON response.

"""

from flask import Blueprint, jsonify, request
from ibkr_api.ib_connection import IBConnection
# from ibkr_api.ib_api import place_order



order_bp = Blueprint('order_routes', __name__)


@order_bp.route('/place_order', methods=['POST'])
def handle_order():
    """
    Place an order using the Interactive Brokers API.
    
    """
    data = request.get_json()

    symbol = data.get('symbol')
    action = data.get('action')
    quantity = data.get('quantity')

    if not symbol or not action or not quantity:
        return jsonify({"error": "Invalid input"}), 400
    
    # ib_conn = ib_connection.get_ib_api()
    
    ib_connection = IBConnection()
    ib_connection.start()

    
    # print(symbol, action, quantity)  
    result = ib_connection.ReqMarketData(symbol)

    # result = place_order(symbol, action, quantity, ib_connection)
    
    return jsonify(result)
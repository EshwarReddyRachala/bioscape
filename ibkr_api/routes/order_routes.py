"""
This module contains the routes for placing and canceling orders using the Interactive Brokers API.

The handle_order function receives a POST request with the order details,
including the symbol, action, and quantity. It extracts the details such as the stock symbol, action (BUY or SELL),
and quantity. It then calls the place_order function from the ibkr_api.ib_api module to place the order using the
Interactive Brokers API.

The cancel_order function receives a POST request with the order ID
and calls the cancel_order function from the ibkr_api.ib_api module to cancel the order.

Both functions return the result of their respective API calls as a JSON response.
"""

from flask import Blueprint, jsonify, request
from ibkr_api.ib_connection import ib_connection

order_bp = Blueprint("order_routes", __name__)


@order_bp.route("/order/<symbol>/<action>/<quantity>", methods=["POST"])
def handle_order(symbol=None, action=None, quantity=None):
    """
    Place an order using the Interactive Brokers API.
    """
    if not symbol or not action or not quantity:
        return jsonify({"error": "Invalid input"}), 400

    ib_connection.connect()

    result = ib_connection.place_order(symbol, action, quantity)

    ib_connection.disconnect()

    return jsonify(result)


@order_bp.route("/cancel_order/<orderid>", methods=["POST"])
def cancel_order(orderid=None):
    """
    Cancel an order using the Interactive Brokers API.
    """
    if not orderid:
        return jsonify({"error": "Order ID is required"}), 400

    ib_connection.connect()

    result = ib_connection.cancel_order(orderid)

    ib_connection.disconnect()

    return jsonify(result)

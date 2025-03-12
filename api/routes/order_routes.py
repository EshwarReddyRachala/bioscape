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

from flask import Blueprint, jsonify
from api.ibkr.ib_app import IBApp

order_bp = Blueprint("order_routes", __name__)


@order_bp.route("/api/order/<symbol>/<action>/<type>/<quantity>", methods=["POST"])
def handle_order(symbol=None, action=None,ordertype=None, quantity=None):
    """
    Place an order using the Interactive Brokers API.
    """
    if not symbol or not action or not quantity:
        return jsonify({"error": "Invalid input"}), 400

    order = IBApp()
    result = order.order_execution(symbol, action, ordertype, int(quantity))

    return jsonify(result)


@order_bp.route("/api/order/cancel/", methods=["POST"])
def cancel_order():
    """
    Cancel an order using the Interactive Brokers API.
    """

    app = IBApp()

    result = app.cancel_last_order()

    return jsonify(result)


@order_bp.route("/api/order/open/", methods=["GET"])
def get_open_orders():
    """
    _summary_

    Returns:
        _type_: _description_

    """
    app = IBApp()

    result = app.get_open_orders()

    return jsonify(result)

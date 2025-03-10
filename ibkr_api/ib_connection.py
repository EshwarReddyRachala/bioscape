"""
This module provides a class to establish a connection to the Interactive Brokers API.

"""

import threading
import time
from ibkr_api.ib_api import IBApi
from ibkr_api.config import Config
from ibapi.contract import Contract
from ibapi.order import Order


class IBConnection:
    """
    Establishes a connection to the Interactive Brokers API.

    This class provides methods to start the API connection and retrieve the IBApi instance.

    """

    def __init__(self):
        self.ib_api = IBApi()
        self.connected = False
        self.next_order_id = None

    def run_loop(self):
        self.ib_api.run()

    def connect(self):
        self.ib_api.connect(
            host=Config.IB_HOST, port=Config.IB_PORT, clientId=Config.IB_CLIENT_ID
        )
        api_thread = threading.Thread(target=self.run_loop, daemon=True)
        api_thread.start()
        
        # while True:
        #     if isinstance(self.ib_api._next_order_id, int):
        #         self.next_order_id = self.ib_api._next_order_id
        #         self.connected = True
        #         break
        #     else:
        #         time.sleep(1)

    def disconnect(self):
        self.ib_api.disconnect()
        self.connected = False
        self.next_order_id = None

    def req_market_data(self, symbol: str):
        """
        Requests market data for a given symbol.

        :param symbol: The symbol for which market data is requested.
        :return: The market data.
        """
        contract = Contract()
        contract.symbol = symbol.strip().upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        result = self.ib_api.reqMktData(1, contract, "", False, False, [])
        time.sleep(10)
        return result

    def place_order(self, symbol: str, action: str, quantity: float):
        """
        Places an order for a given symbol and quantity.

        :param symbol: The symbol for which the order is placed.
        :param action: The action of the order (either 'BUY' or 'SELL').
        :param quantity: The quantity of the order.
        :return: A dictionary with the status of the order placement.
        """
        # Create and configure the Contract object for the given symbol.
        contract = Contract()
        contract.symbol = symbol.strip().upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        # Create and configure the Order object.
        order = Order()
        order.action = action.strip().upper()
        if order.action not in ("BUY", "SELL"):
            raise ValueError("Invalid action: must be either 'BUY' or 'SELL'.")

        order.totalQuantity = float(quantity)
        if order.totalQuantity <= 0:
            raise ValueError("Quantity must be a positive number.")

        order.orderType = "MKT"

        # Place the order.
        try:
            orderID = self.ib_api.get_next_order_id()
            self.ib_api.placeOrder(orderID, contract, order)
            return {"status": "Order placed", "order_id": orderID}

        except Exception as e:
            return {"error": f"Failed to place order: {str(e)}"}



ib_connection = IBConnection()
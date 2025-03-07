from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.common import TickType
from ibkr_api.logging_setup import logger

class IBApi(EWrapper, EClient):
    """Interact with the Interactive Brokers API."""

    def __init__(self):
        """Initialize the Interactive Brokers API."""
        EClient.__init__(self, self)

    def next_valid_id(self, order_id: int):
        """Set the next valid order ID."""
        super().nextValidId(order_id)
        self.next_valid_id = order_id

    def error(self, req_id, error_code, error_string):
        """Log an error message."""
        logger.error(f"Error: {req_id}, {error_code}, {error_string}")

    def order_status(self, order_id, status, filled, remaining, avg_fill_price, perm_id,
                     parent_id, last_fill_price, client_id, why_held, mkt_cap_price):
        """Log an order status message."""
        logger.info(f"Order Status - ID: {order_id}, Status: {status}, Filled: {filled}, Remaining: {remaining}")

    def exec_details(self, req_id, contract, execution):
        """Log an execution details message."""
        logger.info(f"Execution Details - ReqID: {req_id}, Symbol: {contract.symbol}, Execution ID: {execution.execId}")

def place_order(symbol, action, quantity, ib_api):
    """Place an order using the Interactive Brokers API."""
    contract = Contract()
    contract.symbol = symbol
    contract.sec_type = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    order = Order()
    order.action = action.upper()
    order.order_type = "MKT"
    order.total_quantity = quantity

    if ib_api.next_valid_id is not None:
        ib_api.place_order(ib_api.next_valid_id, contract, order)
        ib_api.next_valid_id += 1
        return {"status": "Order placed", "order_id": ib_api.next_valid_id - 1}
    else:
        return {"error": "Order ID not initialized yet"}


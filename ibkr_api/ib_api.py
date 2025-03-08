from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibkr_api.logging_setup import logger

# from ibapi.common import TickType

class IBApi(EWrapper, EClient):
    
    """Interact with the Interactive Brokers API."""

    def __init__(self):
        EClient.__init__(self, self)
        self.next_order_id = None  # ✅ Ensure this attribute is initialized

    def nextValidId(self, orderId: int):
        """This method is called when the API connects and provides the next valid order ID."""
        super().nextValidId(orderId)
        self.next_order_id = orderId  # ✅ Set next_order_id properly
        print(f"Next valid order ID: {orderId}")

    def error(self, reqId, errorCode, errorString):
        """Log an error message."""
        logger.error("Error: %s, %s, %s", reqId, errorCode, errorString)

    
    def order_status(self, order_id, status, filled, remaining):
        """Log an order status message."""
        logger.info("Order Status - ID: %s, Status: %s, Filled: %s, Remaining: %s", 
                    order_id, status, filled, remaining)
    
    def exec_details(self, req_id, contract, execution):
        """Log an execution details message."""
        logger.info("Execution Details - ReqID: %s, Symbol: %s, Execution ID: %s", req_id, contract.symbol, execution.execId)
        
def place_order(symbol, action, quantity, ib_api):
    """
    Place an order using the Interactive Brokers API.
    :param symbol: The stock symbol.
    :param action: The order action (BUY or SELL).
    :param quantity: The order quantity.
    :param ib_api: The Interactive Brokers API instance.
    :return: A dictionary indicating the status of the order.
    """
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
        ib_api.placeOrder(ib_api.next_order_id, contract, order)  # ✅ Correct Method Name
        ib_api.next_valid_id += 1
        return {"status": "Order placed", "order_id": ib_api.next_valid_id - 1}
    else:
        return {"error": "Order ID not initialized yet"}
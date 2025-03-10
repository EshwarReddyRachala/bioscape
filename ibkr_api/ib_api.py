from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibkr_api.logging_setup import logger

class IBApi(EWrapper, EClient):
    """Interact with the Interactive Brokers API."""

    def __init__(self):
        EClient.__init__(self, self)
        self._next_order_id = None

    def nextValidId(self, next_order_id: int):
        """This method is called when the API connects and provides the next valid order ID."""
        super().nextValidId(next_order_id)
        self._next_order_id = next_order_id
        logger.info("Next valid order ID: %s", next_order_id)
        
    def get_next_order_id(self):
        """ Returns the next order ID and increments it for future orders. """
        if self._next_order_id is None:
            raise ValueError("Next order ID is not set yet. Ensure IB is connected.")
        order_id = self._next_order_id
        self._next_order_id += 1  # 🔥 Manually increment order ID
        return order_id

    def error(self, req_id: int, error_code: int, error_string: str, advanced_order_reject_json: str = ""):
        """Log an error message."""
        logger.error("Error: %s, %s, %s", req_id, error_code, error_string)
        if advanced_order_reject_json:
            logger.error("Advanced Order Reject Info: %s", advanced_order_reject_json)

    def order_status(self, order_id: int, status: str, filled: int, remaining: int):
        """Log an order status message."""
        logger.info("Order Status - ID: %s, Status: %s, Filled: %s, Remaining: %s", 
                    order_id, status, filled, remaining)
    
    def open_order(self, order_id: int, contract, order, order_state):
        """Log an open order message."""
        logger.info("Open Order - ID: %s, Symbol: %s, SecType: %s, Exchange: %s, Action: %s, Type: %s, Quantity: %s, Status: %s", 
                    order_id, contract.symbol, contract.secType, contract.exchange, order.action, order.orderType, order.totalQuantity, order_state.status)
    
    def exec_details(self, req_id: int, contract, execution):
        """Log an execution details message."""
        logger.info("Execution Details - ReqID: %s, Symbol: %s, Execution ID: %s", req_id, contract.symbol, execution.execId)


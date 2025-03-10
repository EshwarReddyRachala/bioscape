from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibkr_api.logging_setup import logger

# from ibapi.common import TickType

class IBApi(EWrapper, EClient):
    
    """Interact with the Interactive Brokers API.
    
    This class inherits from the EWrapper and EClient classes provided by the Interactive Brokers API.
    It provides methods to interact with the API, such as placing orders and receiving market data.
    
    Attributes:
        next_order_id (int): The next available order ID.
    """

    def __init__(self):
        EClient.__init__(self, self)
        self.next_order_id = None  # ✅ Ensure this attribute is initialized

    def nextValidId(self, orderId: int):
        """This method is called when the API connects and provides the next valid order ID."""
        super().nextValidId(orderId)
        self.next_order_id = orderId  # ✅ Set next_order_id properly
        print(f"Next valid order ID: {orderId}")

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        print(f"Error: {reqId}, {errorCode}, {errorString}")
        logger.error("Error: %s, %s, %s", reqId, errorCode, errorString)
        if advancedOrderRejectJson:
            print(f"Advanced Order Reject Info: {advancedOrderRejectJson}")

    
    def order_status(self, order_id, status, filled, remaining):
        """Log an order status message."""
        logger.info("Order Status - ID: %s, Status: %s, Filled: %s, Remaining: %s", 
                    order_id, status, filled, remaining)
    
    def openOrder(self, orderId, contract, order, orderState):
        logger.info('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', 
                    order.action, order.orderType, order.totalQuantity, orderState.status)
    
    def exec_details(self, req_id, contract, execution):
        """Log an execution details message."""
        logger.info("Execution Details - ReqID: %s, Symbol: %s, Execution ID: %s", req_id, contract.symbol, execution.execId)
        

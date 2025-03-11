from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from api.logging_setup import logger


class IBApi(EWrapper, EClient):
    """Interact with the Interactive Brokers API."""

    def __init__(self):
        EClient.__init__(self, self)
        self._next_order_id = None

    def nextValidId(self, orderId: int):
        """This method is called when the API connects and provides the next valid order ID."""
        super().nextValidId(orderId)
        self._next_order_id = orderId
        logger.info("Next valid order ID: %s", orderId)

    def error(
        self,
        req_id: int,
        error_code: int,
        error_string: str,
        advanced_order_reject_json: str = "",
    ):
        """Log an error message."""
        logger.error("Error: %s, %s, %s", req_id, error_code, error_string)
        if advanced_order_reject_json:
            logger.error("Advanced Order Reject Info: %s", advanced_order_reject_json)

    def order_status(self, order_id: int, status: str, filled: int, remaining: int):
        """Log an order status message."""
        logger.info(
            "Order Status - ID: %s, Status: %s, Filled: %s, Remaining: %s",
            order_id,
            status,
            filled,
            remaining,
        )

    def open_order(self, order_id: int, contract, order, order_state):
        """Log an open order message."""
        logger.info(
            "Open Order - ID: %s, Symbol: %s, SecType: %s, Exchange: %s, Action: %s, Type: %s, Quantity: %s, Status: %s",
            order_id,
            contract.symbol,
            contract.secType,
            contract.exchange,
            order.action,
            order.orderType,
            order.totalQuantity,
            order_state.status,
        )

    def exec_details(self, req_id: int, contract, execution):
        """Log an execution details message."""
        logger.info(
            "Execution Details - ReqID: %s, Symbol: %s, Execution ID: %s",
            req_id,
            contract.symbol,
            execution.execId,
        )

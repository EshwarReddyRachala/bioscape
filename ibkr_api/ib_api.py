from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibkr_api.logging_setup import logger

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.next_order_id = None

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.next_order_id = orderId
        logger.info(f"Next valid order ID: {orderId}")

    def error(self, reqId, errorCode, errorString):
        logger.error(f"Error: {reqId}, {errorCode}, {errorString}")

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        logger.info(f"Order Status - ID: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}")

    def execDetails(self, reqId, contract, execution):
        logger.info(f"Execution Details - ReqID: {reqId}, Symbol: {contract.symbol}, Execution ID: {execution.execId}")

def place_order(symbol, action, quantity, ib_api):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    order = Order()
    order.action = action.upper()
    order.orderType = "MKT"
    order.totalQuantity = quantity

    if ib_api.next_order_id is not None:
        ib_api.placeOrder(ib_api.next_order_id, contract, order)
        ib_api.next_order_id += 1
        return {"status": "Order placed", "order_id": ib_api.next_order_id - 1}
    else:
        return {"error": "Order ID not initialized yet"}

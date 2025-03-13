from threading import Thread
import time
from ibapi.contract import Contract
from ibapi.order import Order

from api.ibkr.ib_client import IBClient
from api.ibkr.ib_wrapper import IBWrapper
from ..util.logging_setup import logger
from ..util.config import Config


class IBApp(IBClient, IBWrapper):
    """_summary_

    Args:
        IBClient (_type_): _description_
        IBWrapper (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Intializes our main classes
    def __init__(self):
        """_summary_

        Args:
            ipaddress (_type_): _description_
            portid (_type_): _description_
            clientid (_type_): _description_
        """
        IBWrapper.__init__(self)
        IBClient.__init__(self, wrapper=self)
        self._next_order_id = None
        self.last_order_id = None

        logger.info("Connecting to the server")

        # Connects to the server with the ipaddress, portid, and clientId specified in the program execution area
        self.connect(Config.IB_HOST, Config.IB_PORT, Config.IB_CLIENT_ID)

        # Initializes the threading
        thread = Thread(target=self.run, daemon=True)
        thread.start()
        setattr(self, "_thread", thread)

        logger.info("Connected to the server")

        # Starts listening for errors
        self.init_error()

    def nextValidId(self, orderId: int):
        """This method is called when the API connects and provides the next valid order ID."""
        super().nextValidId(orderId)
        self._next_order_id = orderId

    def getorder_id(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        while self._next_order_id is None:
            time.sleep(0.1)

            # Define the local order ID
        orderid = self._next_order_id

        if orderid == self.last_order_id:
            orderid += 1

        self.last_order_id = orderid

        logger.info("Order ID: %s", orderid)

        return orderid

    def disconnect(self):
        """
        _summary_

        Returns:
            _type_: _description_

        """
        logger.info("Disconnecting from the server")

        return super().disconnect()

    def contract(self, symbol: str):
        """_summary_

        Args:
            symbol (str): _description_

        Returns:
            _type_: _description_
        """
        # Fills out the contract object
        contract1 = Contract()  # Creates a contract object from the import
        contract1.symbol = symbol.strip().upper()  # Sets the ticker symbol
        contract1.secType = "STK"  # Defines the security type as stock
        contract1.currency = "USD"  # Currency is US dollars
        # In the API side, NASDAQ is always defined as ISLAND in the exchange field
        contract1.exchange = "SMART"
        # contract1.PrimaryExch = "NYSE"
        logger.info("Contract: %s", contract1)

        return contract1  # Returns the contract object

    def order(self, action: str, ordertype: str, quantity: int):
        """_summary_

        Args:
            action (str): _description_
            ordertype (str): _description_
            quantity (int): _description_

        Returns:
            _type_: _description_
        """
        # Fills out the order object
        order1 = Order()  # Creates an order object from the import
        order1.action = action.strip().upper()  # Sets the order action to buy
        order1.orderType = ordertype.strip().upper()  # Sets order type to market buy
        order1.transmit = True
        order1.eTradeOnly = False 
        order1.firmQuoteOnly = False
        order1.totalQuantity = quantity  # Setting a static quantity of 10
        logger.info("Order ID: %s", order1)
        return order1  # Returns the order object

    def order_execution(self, symbol: str, action: str, ordertype: str, quantity: int):
        """
        Places an order based on the provided symbol, action, order type, and quantity.

        This method performs the following steps:
          1. Creates a contract object for the specified symbol.
          2. Creates an order object using the given action, order type, and quantity.
          3. Retrieves a unique order ID.
          4. Places the order by combining the contract and order objects.
          5. Prints a confirmation message upon successfully placing the order.

        Parameters:
            symbol (str): The asset symbol for which the order is to be placed.
            action (str): The order action, such as "BUY" or "SELL".
            ordertype (str): The type of order (e.g., "MARKET", "LIMIT").
            quantity (int): The number of shares or contracts to trade.

        Returns:
            None.
        """
        try:
            contract_obj = self.contract(symbol)
            order_obj = self.order(
                action=action, ordertype=ordertype, quantity=quantity
            )
            next_id = self.getorder_id()
            logger.info("Order ID: %s", next_id)
            logger.info("Submitting order")
            self.placeOrder(next_id, contract_obj, order_obj)

            logger.info(ordertype + " " + action +
                        " order was placed for : " + symbol)

            self.disconnect()

            logger.info("Disconnected from the server")

            return {"status": "Order placed", "order_id": next_id}

        except Exception as e:

            return {"error": f"Failed to place order: {str(e)}"}

    def cancel_order(self, order_id: int):
        """
        _summary_

        Args:
            order_id (int): _description_

        Returns:
            _type_: _description_
        """
        super().cancelOrder(order_id)

        return {"status": "Order canceled", "order_id": order_id}

    def cancel_last_order(self):
        """
        _summary_

        Returns:
            _type_: _description_
        """
        self.cancel_order(self.last_order_id)

        return {"status": "Order canceled", "order_id": self.last_order_id}

    def get_open_orders(self):
        """
        _summary_

        Returns:
            _type_: _description_
        """

        return self.reqOpenOrders()

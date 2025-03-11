from threading import Thread
import time

from api.ibkr.ib_client import IBClient
from api.ibkr.ib_wrapper import IBWrapper
from ibapi.contract import Contract
from ibapi.order import Order
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

    def getOrderID(self):
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

        logger.info(f"Order ID: {orderid}")

        return orderid

    def disconnect(self):
        """
        _summary_

        Returns:
            _type_: _description_

        """
        logger.info("Disconnecting from the server")

        return super().disconnect()

    def contractCreate(self, symbol: str):
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
        logger.info(f"Contract: {contract1}")
        return contract1  # Returns the contract object

    def orderCreate(self, action: str, ordertype: str, quantity: int):
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
        order1.totalQuantity = quantity  # Setting a static quantity of 10
        logger.info(f"Order: {order1}")
        return order1  # Returns the order object

    def orderExecution(self, symbol: str, action: str, ordertype: str, quantity: int):
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
        # Places the order with the returned contract and order objects
        contractObject = self.contractCreate(symbol)
        orderObject = self.orderCreate(
            action=action, ordertype=ordertype, quantity=quantity
        )
        nextID = self.getOrderID()
        logger.info(f"Order ID: {nextID}")
        logger.info("Submitting order")
        self.placeOrder(nextID, contractObject, orderObject)
        logger.info("order was placed")

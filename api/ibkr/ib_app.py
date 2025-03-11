from threading import Thread
import time

from api.ibkr.ib_client import IBClient
from api.ibkr.ib_wrapper import IBWrapper
from ibapi.contract import Contract
from ibapi.order import Order


class IBApp(IBClient, IBWrapper):
    # Intializes our main classes
    def __init__(self, ipaddress, portid, clientid):
        IBWrapper.__init__(self)
        IBClient.__init__(self, wrapper=self)
        self._next_order_id = None
        self.last_order_id = None

        # Connects to the server with the ipaddress, portid, and clientId specified in the program execution area
        self.connect(ipaddress, portid, clientid)

        # Initializes the threading
        thread = Thread(target=self.run)
        thread.start()
        setattr(self, "_thread", thread)

        # Starts listening for errors
        self.init_error()

    def nextValidId(self, orderId: int):
        """This method is called when the API connects and provides the next valid order ID."""
        super().nextValidId(orderId)
        self._next_order_id = orderId

    def getOrderID(self):
        while self._next_order_id is None:
            time.sleep(0.1)

            # Define the local order ID
        orderid = self._next_order_id

        if orderid == self.last_order_id:
            orderid += 1

        self.last_order_id = orderid
        return orderid

    def disconnect(self):
        return super().disconnect()

    def contractCreate(self, symbol: str):
        # Fills out the contract object
        contract1 = Contract()  # Creates a contract object from the import
        contract1.symbol = symbol.strip().upper()  # Sets the ticker symbol
        contract1.secType = "STK"  # Defines the security type as stock
        contract1.currency = "USD"  # Currency is US dollars
        # In the API side, NASDAQ is always defined as ISLAND in the exchange field
        contract1.exchange = "SMART"
        # contract1.PrimaryExch = "NYSE"
        return contract1  # Returns the contract object

    def orderCreate(self, action: str, ordertype: str, quantity: int):
        # Fills out the order object
        order1 = Order()  # Creates an order object from the import
        order1.action = action.strip().upper()  # Sets the order action to buy
        order1.orderType = ordertype.strip().upper()  # Sets order type to market buy
        order1.transmit = True
        order1.totalQuantity = quantity  # Setting a static quantity of 10
        return order1  # Returns the order object

    def orderExecution(self, symbol: str, action: str, ordertype: str, quantity: int):
        # Places the order with the returned contract and order objects
        contractObject = self.contractCreate(symbol)
        orderObject = self.orderCreate(
            action=action, ordertype=ordertype, quantity=quantity
        )
        nextID = self.getOrderID()
        self.placeOrder(nextID, contractObject, orderObject)
        print("order was placed")

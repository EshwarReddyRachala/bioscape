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
        """
        Initializes the IBConnection class.

        :return: None
        
        """
        self._ib_api = IBApi()  # Create an instance of IBApi
        self.connected = False
        self.next_order_id = None
        
    def run_loop(self):
        self._ib_api.run()

    def start(self):
        """
        Starts the API connection.

        This method connects to the Interactive Brokers API using the configured host, port, and client ID.
        It also starts a new thread to run the API in the background.

        :return: None
        """
        self._ib_api.connect(
            host=Config.IB_HOST,
            port=Config.IB_PORT,
            clientId=Config.IB_CLIENT_ID
        )
        api_thread = threading.Thread(target=self.run_loop, daemon=True)
        api_thread.start()
        
        while True:
            if isinstance(self._ib_api.next_order_id, int):
                
                print("Next valid order ID received.", self._ib_api.next_order_id)
                self.next_order_id = self._ib_api.next_order_id
                self.connected = True
                print("✅ Connected to IBKR API!")
                break
            else:
                print("Waiting for next valid order ID...")
                time.sleep(1)    
                
                
    def ReqMarketData(self,symbol:str):
        
        #Create contract object
        apple_contract = Contract()
        apple_contract.symbol = 'AAPL'
        apple_contract.secType = 'STK'
        apple_contract.exchange = 'SMART'
        apple_contract.currency = 'USD'


        result = self._ib_api.reqMktData(1, apple_contract, '', False, False, [])
        
        time.sleep(10)
        
        return result
           
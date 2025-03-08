"""
This module provides a class to establish a connection to the Interactive Brokers API.

"""
import threading
import time
from ibkr_api.ib_api import IBApi
from ibkr_api.config import Config



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
        self._ib_api = IBApi()

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
        api_thread = threading.Thread(target=self._ib_api.run, daemon=True)
        api_thread.start()

        timeout = 10  # Maximum wait time in seconds
        start_time = time.time()
        while self._ib_api.next_order_id is None:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timed out waiting for next valid order ID.")
        print("Waiting for next valid order ID...")
        time.sleep(1)

    def get_ib_api(self):
        """
        Returns the IBApi instance.

        :return: The IBApi instance."""

        return self._ib_api


ib_connection = IBConnection()
ib_connection.start()

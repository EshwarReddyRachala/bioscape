from ibkr_api.ib_api import IBApi
import threading
from ibkr_api.config import Config


class IBConnection:
    """
    Establishes a connection to the Interactive Brokers API.

    This class provides methods to start the API connection and retrieve the IBApi instance.

    """
    def __init__(self):
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

    def get_ib_api(self):
        """
        Returns the IBApi instance.

        :return: The IBApi instance."""

        return self._ib_api


ib_connection = IBConnection()
ib_connection.start()

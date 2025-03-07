from ibkr_api.ib_api import IBApi
import threading
from ibkr_api.config import Config


class IBConnection:
    def __init__(self):
        self._ib_api = IBApi()

    def start(self):
        self._ib_api.connect(
            host=Config.IB_HOST,
            port=Config.IB_PORT,
            client_id=Config.IB_CLIENT_ID
        )
        api_thread = threading.Thread(target=self._ib_api.run, daemon=True)
        api_thread.start()

    def get_ib_api(self):
        return self._ib_api


ib_connection = IBConnection()
ib_connection.start()


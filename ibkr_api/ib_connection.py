from ibkr_api.ib_api import IBApi
import threading
from ibkr_api.config import Config

class IBConnection:
    def __init__(self):
        self.ib_api = IBApi()

    def start(self):
        self.ib_api.connect(Config.IB_HOST, Config.IB_PORT, Config.IB_CLIENT_ID)
        api_thread = threading.Thread(target=self.ib_api.run, daemon=True)
        api_thread.start()

    def get_ib_api(self):
        return self.ib_api

ib_connection = IBConnection()
ib_connection.start()

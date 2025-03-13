from threading import Thread
import queue
import datetime
import time
from ibapi.wrapper import *
from ibapi.client import *
from ibapi.contract import *
from ibapi.order import *
from ..util.logging_setup import logger

class IBClient(EClient):
    """_Initializes the client_"""

    def __init__(self, wrapper):
        """_Initializes the client_"""
        ## Set up with a wrapper inside
        logger.info("IBClient: Initializing")
        EClient.__init__(self, wrapper)

    def server_clock(self):
        """_Requests the unix time from the server_"""

        print("Asking server for Unix time")

        # Creates a queue to store the time
        time_storage = self.wrapper.init_time()

        # Sets up a request for unix time from the Eclient
        self.reqCurrentTime()

        # Specifies a max wait time if there is no connection
        max_wait_time = 10

        try:
            requested_time = time_storage.get(timeout=max_wait_time)
        except queue.Empty:
            print("The queue was empty or max time reached")
            requested_time = None

        while self.wrapper.is_error():
            print("Error:")
            # print(self.get_error(timeout=5))

        return requested_time

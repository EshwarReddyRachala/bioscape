import queue
from ibapi.wrapper import *
from threading import Thread
import queue
import datetime
import time
from ..util.logging_setup import logger

class IBWrapper(EWrapper):

    ## error handling code
    def init_error(self):
        logger.info("Initializing error")
        error_queue = queue.Queue()
        self.my_errors_queue = error_queue

    def is_error(self):
        error_exist = not self.my_errors_queue.empty()
        return error_exist

    def get_error(self, timeout=6):
        if self.is_error():
            try:
                return self.my_errors_queue.get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def error(
        self, reqId: int, errorCode: int, errorString: str, advancedOrderRejectJson=""
    ):
        print(f"Error: reqId={reqId}, errorCode={errorCode}, errorMsg={errorString}")
        if advancedOrderRejectJson:
            print(f"Advanced Order Reject: {advancedOrderRejectJson}")

    def init_time(self):
        time_queue = queue.Queue()
        self.my_time_queue = time_queue
        return time_queue

    def currentTime(self, server_time):
        ## Overriden method
        self.my_time_queue.put(server_time)

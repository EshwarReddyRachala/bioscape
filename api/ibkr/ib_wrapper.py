import queue
from threading import Thread
import queue
import datetime
import time
from ibapi.wrapper import *
from ..util.logging_setup import logger

class IBWrapper(EWrapper):
    """
    Wrapper class for the IBKR API.
    
    Attributes:
        _thread (Thread): The thread object representing the wrapper's execution.
        my_errors_queue (queue.Queue): A queue to store error messages.
        my_time_queue (queue.Queue): A queue to store time information.
    """

    ## error handling code
    def init_error(self):
        """
        Initializes the error queue.
        """
        logger.info("Initializing error")
        error_queue = queue.Queue()
        self.my_errors_queue = error_queue

    def is_error(self):
        """
        Summary 
        """
        error_exist = not self.my_errors_queue.empty()
        return error_exist

    def get_error(self, timeout=6):
        """
        Gets an error message from the error queue.

        Args:
            timeout (int, optional): The maximum number of seconds to wait for an error message. Defaults to 6.

        Returns:
            str: The error message if available, otherwise None.
        """
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
        """
        Initializes the time queue.
        """
        logger.info("Initializing time")
        time_queue = queue.Queue()
        self.my_time_queue = time_queue
        return time_queue

    def currentTime(self, server_time):
        """ Current time"""
        ## Overriden method
        self.my_time_queue.put(server_time)

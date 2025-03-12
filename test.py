"""
This is a test file for the IBKR API
"""
import time
from api.ibkr.ib_app import IBApp

if __name__ == "__main__":
    # Create app instance
0    app = IBApp()
    # A printout to show the program began
    print("The program has begun")

    # assigning the return from our clock method to a variable
    requested_time = app.server_clock()

   

    print("order was placed")
    app.order_execution("SPYI", "BUY", "MKT", 100)

    # printing the return from the server
    print("")
    print("This is the current time from the server ")
    contract = app.contract("PYPL")
    app.reqMktData(1, contract, "", False, False, [])
    time.sleep(10)
    
    app.disconnect()

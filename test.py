from api.ibkr.ib_app import IBApp
import time

if __name__ == "__main__":
    # Create app instance
    app = IBApp()
    # A printout to show the program began
    print("The program has begun")

    # assigning the return from our clock method to a variable
    requested_time = app.server_clock()

    time1 = app.currentTime(requested_time)
    print("order was placed")
    app.orderExecution("TSLL", "BUY", "MKT", 100)

    # printing the return from the server
    print("")
    print("This is the current time from the server ")
    print(time1)
    contract = app.contractCreate("PYPL")
    app.reqMktData(1, contract, "", False, False, [])
    time.sleep(10)
    
    app.disconnect()

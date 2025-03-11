from api.config import Config
from api.ibkr.ib_app import IBApp


if __name__ == '__main__':
    # Create app instance
    app = IBApp(Config.IB_HOST, Config.IB_PORT, Config.IB_CLIENT_ID)
    # A printout to show the program began
    print("The program has begun")

        #assigning the return from our clock method to a variable 
    requested_time = app.server_clock()
    
    time = app.currentTime(requested_time)
    app.BUY('AMZN','BUY','MKT', 100)
    print("order was placed")
    
    #printing the return from the server
    print("")
    print("This is the current time from the server " )
    print(time)
    
    app.orderExecution('AMZN', 'BUY', 'MKT', 100)
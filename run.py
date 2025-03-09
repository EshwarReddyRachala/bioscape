"""
This script runs the Flask application using the development server.
    
    - The Flask application is created using the create_app() function from ibkr_api.app module.
    - The application is run on the host and port specified in the Config class from ibkr_api.config module.
    - The debug mode is set to the value specified in the Config class.
    
    Usage:
        python run.py
        
    Note:
        Ensure the necessary dependencies are installed and the ibkr_api package is available in the Python path.
        The Flask application is run using the development server. For production, consider using a production server.
        The Flask application is run on the host and port specified in the Config class. Update the values as needed.
        The debug mode is set to the value specified in the Config class. Update the value as needed.
        
    Author: Firstname Lastname
    Date: 2023-08-30
    Version: 1.0
"""

from ibkr_api.app import create_app
from ibkr_api.config import Config

application = create_app()

if __name__ == "__main__":
    application.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
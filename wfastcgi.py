import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

from api.app import create_app

# Create app instance
app = create_app()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

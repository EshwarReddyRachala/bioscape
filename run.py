from ibkr_api.app import create_app
from ibkr_api.config import Config

application = create_app()

if __name__ == "__main__":
    application.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)


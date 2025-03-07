from ibkr_api.app import create_app
from ibkr_api.config import Config

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=True)

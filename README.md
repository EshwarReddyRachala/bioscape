# IBKR API

## Overview

This project is a Flask-based API that integrates with Interactive Brokers (IBKR) using the `ibapi` package. It provides endpoints to place stock orders and check the API status.

## Prerequisites

Ensure you have the following installed on your system:

- Python (>=3.8)
- Pip
- Virtual environment (`venv`)
- Interactive Brokers Trader Workstation (TWS) or IB Gateway

## Setting Up the Project

### 1. Clone the Repository

```sh
git clone https://github.com/EshwarReddyRachala/bioscape.git
cd bioscape
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

#### **Linux/macOS**

```sh
python3 -m venv venv
source venv/bin/activate
```

#### **Windows**

```sh
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Ensure `pip` is up to date before installing the required dependencies.

```sh
pip install --upgrade pip
pip freeze > requirements.txt
pip install -r requirements.txt
```

### 4. Running the API

Start the Flask application using:

```sh
python run.py
```

By default, the API runs on `http://127.0.0.1:5000`.

## API Endpoints

### 1. Check API Status

**Endpoint:**

```http
GET /status
```

**Response:**

```json
{
  "status": "API is running"
}
```

### 2. Place a Stock Order

**Endpoint:**

```http
POST /place_order
```

**Request Body (JSON):**

```json
{
  "symbol": "AAPL",
  "action": "BUY",
  "quantity": 10
}
```

**Response:**

```json
{
  "status": "Order placed",
  "order_id": 1
}
```

## Managing Dependencies

If you install new packages, update `requirements.txt` using:

```sh
pip freeze > requirements.txt
```

To remove unused dependencies:

```sh
pip uninstall -r requirements.txt -y
pip freeze > requirements.txt
```

## Troubleshooting

### 1. Virtual Environment Not Activating

Ensure you are using the correct command:

- **Windows**: `venv\Scripts\activate`
- **Linux/macOS**: `source venv/bin/activate`

### 2. Dependency Conflicts

If you encounter dependency issues, try:

```sh
pip install --upgrade --no-cache-dir -r requirements.txt
```

Or manually resolve conflicts by checking:

```sh
pip check
```

### 3. Connection Issues with IBKR

- Ensure TWS or IB Gateway is running.
- Enable API connections in IB Gateway: `Settings -> API -> Enable ActiveX and Socket Clients`.

## License

This project is licensed under the MIT License.

bioscape llc


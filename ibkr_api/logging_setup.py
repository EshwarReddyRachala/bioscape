"""
Logging setup for the IBKR API package.

This module provides a basic logging configuration for the IBKR API package.
"""

import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

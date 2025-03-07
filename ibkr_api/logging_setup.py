import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

FORMATTER = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

HANDLER = logging.StreamHandler()
HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(HANDLER)

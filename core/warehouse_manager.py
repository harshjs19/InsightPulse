import sqlite3

from config.settings import ANALYTICS_DB, WAREHOUSE_DIR
from core.logger import logger


def initialize_warehouse():
    """Create the analytics warehouse if it doesn't already exist."""

    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(ANALYTICS_DB):
        pass

    logger.info(f"Warehouse ready: {ANALYTICS_DB.name}")

    return ANALYTICS_DB
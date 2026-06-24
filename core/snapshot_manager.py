import shutil

from config.settings import MARKET_DB, RAW_DATA_DIR
from core.logger import logger


SNAPSHOT_NAME = "market_latest.db"


def create_snapshot():
    """Create a fresh snapshot of the AlphaLens database."""

    if not MARKET_DB.exists():
        raise FileNotFoundError(f"Source database not found: {MARKET_DB}")

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    snapshot_path = RAW_DATA_DIR / SNAPSHOT_NAME

    shutil.copy2(MARKET_DB, snapshot_path)

    logger.info(f"Snapshot created: {snapshot_path.name}")

    return snapshot_path
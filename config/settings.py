from pathlib import Path

# ==========================================
# Project Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

WAREHOUSE_DIR = DATA_DIR / "warehouse"

REPORTS_DIR = PROJECT_ROOT / "reports"

# ==========================================
# AlphaLens
# ==========================================

# Change this if AlphaLens moves

ALPHALENS_ROOT = Path(r"D:\Projects\AlphaLens")

MARKET_DB = ALPHALENS_ROOT / "db" / "market.db"

# ==========================================
# InsightPulse Warehouse
# ==========================================

ANALYTICS_DB = WAREHOUSE_DIR / "analytics.db"
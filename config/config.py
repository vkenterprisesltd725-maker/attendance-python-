import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
DB_DIR = BASE_DIR / "database"

# Ensure directories exist
for directory in [DATA_DIR, MODELS_DIR, REPORTS_DIR, DB_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Application settings
APP_NAME = "Student Performance & Academic Risk Prediction System"
APP_VERSION = "1.0.0"

# Database
DB_PATH = DB_DIR / "student_performance.db"

# Model
MODEL_PATH = MODELS_DIR / "risk_model.joblib"

# Supported files for import
SUPPORTED_FILE_EXTENSIONS = [".csv", ".xlsx"]

# ML & Prediction thresholds
RISK_THRESHOLDS = {
    "LOW": 0.3,
    "MEDIUM": 0.7,
    "HIGH": 1.0
}

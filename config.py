import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DB_PATH = os.environ.get("ATTENDLY_DB", str(DATA_DIR / "attendly.db"))
STUDENTS_DIR = DATA_DIR / "students"
MODEL_PATH = DATA_DIR / "models" / "trainer.yml"
LABELS_PATH = DATA_DIR / "models" / "labels.json"
CASCADE_PATH = DATA_DIR / "haarcascade_frontalface_default.xml"

CAMERA_INDEX = int(os.environ.get("ATTENDLY_CAMERA_INDEX", "0"))
SAMPLES_PER_STUDENT = 30
RECOGNITION_CONFIDENCE_THRESHOLD = 65  # lower LBPH distance = better match

REPORT_EMAIL_TO = os.environ.get("ATTENDLY_REPORT_EMAIL", "")
SMTP_HOST = os.environ.get("ATTENDLY_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("ATTENDLY_SMTP_PORT", "587"))
SMTP_USER = os.environ.get("ATTENDLY_SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("ATTENDLY_SMTP_PASSWORD", "")

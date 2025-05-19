import json

import config

SETTINGS_PATH = config.DATA_DIR / "settings.json"

DEFAULTS = {
    "camera_index": config.CAMERA_INDEX,
    "confidence_threshold": config.RECOGNITION_CONFIDENCE_THRESHOLD,
    "report_email": config.REPORT_EMAIL_TO,
}


def load():
    if not SETTINGS_PATH.exists():
        return dict(DEFAULTS)
    with open(SETTINGS_PATH) as f:
        return {**DEFAULTS, **json.load(f)}


def save(values: dict):
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(values, f, indent=2)

    # apply immediately so the running process reflects the change without a restart
    config.CAMERA_INDEX = values["camera_index"]
    config.RECOGNITION_CONFIDENCE_THRESHOLD = values["confidence_threshold"]
    config.REPORT_EMAIL_TO = values["report_email"]

import json

import cv2

import config
from core import database
from core.detector import find_faces

_recognizer = None
_label_map = None


def _load():
    global _recognizer, _label_map
    if _recognizer is None:
        _recognizer = cv2.face.LBPHFaceRecognizer_create()
        _recognizer.read(str(config.MODEL_PATH))
        with open(config.LABELS_PATH) as f:
            _label_map = {int(k): v for k, v in json.load(f).items()}
    return _recognizer, _label_map


def recognize_frame(frame):
    """Detect + identify every face in a BGR frame.

    Returns a list of dicts: {box, student_id, name, confidence, matched}.
    """
    recognizer, label_map = _load()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    results = []
    for (x, y, w, h) in find_faces(gray):
        face = gray[y : y + h, x : x + w]
        label_id, confidence = recognizer.predict(face)

        matched = confidence <= config.RECOGNITION_CONFIDENCE_THRESHOLD
        student_id = label_map.get(label_id) if matched else None
        student = database.get_student(student_id) if student_id else None

        results.append(
            {
                "box": (x, y, w, h),
                "student_id": student_id,
                "name": student["name"] if student else "Unknown",
                "confidence": round(float(confidence), 1),
                "matched": matched,
            }
        )

    return results

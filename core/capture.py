import cv2

import config
from core import database
from core.detector import find_faces


def capture_face_samples(student_id: str, name: str, program: str = ""):
    """Open the webcam, grab SAMPLES_PER_STUDENT face crops, and save them to disk.

    Registers the student in the database first so a partial capture still
    leaves a usable record.
    """
    database.add_student(student_id, name, program)

    student_dir = config.STUDENTS_DIR / student_id
    student_dir.mkdir(parents=True, exist_ok=True)

    cam = cv2.VideoCapture(config.CAMERA_INDEX)
    saved = 0

    try:
        while saved < config.SAMPLES_PER_STUDENT:
            ok, frame = cam.read()
            if not ok:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for (x, y, w, h) in find_faces(gray):
                saved += 1
                face = gray[y : y + h, x : x + w]
                cv2.imwrite(str(student_dir / f"{saved}.jpg"), face)
                if saved >= config.SAMPLES_PER_STUDENT:
                    break
    finally:
        cam.release()

    return saved

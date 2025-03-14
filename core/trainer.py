import json

import cv2
import numpy as np

import config


def train_model():
    """Train an LBPH recognizer on every captured student image.

    Returns the number of students trained on. Raises ValueError if no
    images have been captured yet.
    """
    images, labels = [], []
    label_map = {}

    student_dirs = sorted(p for p in config.STUDENTS_DIR.iterdir() if p.is_dir())
    if not student_dirs:
        raise ValueError("No captured student images found — run registration first.")

    for label_id, student_dir in enumerate(student_dirs):
        student_id = student_dir.name
        label_map[label_id] = student_id

        for image_path in student_dir.glob("*.jpg"):
            img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            images.append(img)
            labels.append(label_id)

    if not images:
        raise ValueError("Student folders exist but contain no readable images.")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(images, np.array(labels))

    config.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    recognizer.save(str(config.MODEL_PATH))

    with open(config.LABELS_PATH, "w") as f:
        json.dump(label_map, f)

    return len(student_dirs)

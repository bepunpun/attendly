import cv2

import config

_cascade = None


def get_cascade():
    global _cascade
    if _cascade is None:
        _cascade = cv2.CascadeClassifier(str(config.CASCADE_PATH))
    return _cascade


def find_faces(gray_frame):
    """Return a list of (x, y, w, h) boxes for every face found in a grayscale frame."""
    cascade = get_cascade()
    return cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(60, 60),
    )

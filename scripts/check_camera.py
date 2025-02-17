"""Standalone sanity check: confirm OpenCV can open the configured camera."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import cv2

import config


def main():
    cam = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cam.isOpened():
        print(f"Could not open camera index {config.CAMERA_INDEX}")
        sys.exit(1)

    ok, frame = cam.read()
    cam.release()

    if not ok:
        print("Camera opened but returned no frame.")
        sys.exit(1)

    h, w = frame.shape[:2]
    print(f"Camera {config.CAMERA_INDEX} OK — frame size {w}x{h}")


if __name__ == "__main__":
    main()

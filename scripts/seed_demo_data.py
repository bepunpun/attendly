"""Populate the database with fake students + attendance so the UI can be
demoed without a webcam or trained model. Doesn't touch data/students/ images."""
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core import database

DEMO_STUDENTS = [
    ("2021331001", "Ava Chen", "CSE"),
    ("2021331002", "Marcus Lee", "CSE"),
    ("2021331003", "Priya Patel", "EEE"),
    ("2021331004", "Diego Ramirez", "CSE"),
    ("2021331005", "Fatima Noor", "BBA"),
    ("2021331006", "Sam O'Connor", "EEE"),
]


def main():
    database.init_db()

    for student_id, name, program in DEMO_STUDENTS:
        if not database.get_student(student_id):
            database.add_student(student_id, name, program)

    today = datetime.now()
    with database.get_conn() as conn:
        for student_id, _, _ in DEMO_STUDENTS:
            for days_ago in range(10):
                if random.random() > 0.75:
                    continue  # simulate the occasional absence
                ts = today - timedelta(days=days_ago, minutes=random.randint(0, 90))
                status = "late" if random.random() < 0.15 else "present"
                conn.execute(
                    "INSERT INTO attendance (student_id, timestamp, status) VALUES (?, ?, ?)",
                    (student_id, ts.isoformat(timespec="seconds"), status),
                )

    print(f"Seeded {len(DEMO_STUDENTS)} students with sample attendance history.")


if __name__ == "__main__":
    main()

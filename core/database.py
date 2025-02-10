import sqlite3
from contextlib import contextmanager
from datetime import date, datetime

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    program TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'present',
    FOREIGN KEY (student_id) REFERENCES students (student_id)
);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)


def add_student(student_id: str, name: str, program: str = ""):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO students (student_id, name, program, created_at) VALUES (?, ?, ?, ?)",
            (student_id, name, program, datetime.now().isoformat(timespec="seconds")),
        )


def get_students():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM students ORDER BY name").fetchall()


def get_student(student_id: str):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()

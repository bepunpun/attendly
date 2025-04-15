from flask import Flask, render_template

import config
from core import database

app = Flask(__name__)


@app.before_request
def _ensure_db():
    database.init_db()


@app.route("/")
def dashboard():
    all_students = database.get_students()
    today_attendance = {row["student_id"]: row for row in database.get_attendance()}

    roster = []
    for student in all_students:
        record = today_attendance.get(student["student_id"])
        roster.append(
            {
                "student_id": student["student_id"],
                "name": student["name"],
                "program": student["program"],
                "status": record["status"] if record else "absent",
            }
        )

    summary = {
        "total": len(roster),
        "present": sum(1 for s in roster if s["status"] == "present"),
        "absent": sum(1 for s in roster if s["status"] == "absent"),
        "late": sum(1 for s in roster if s["status"] == "late"),
    }

    return render_template(
        "dashboard.html", active="home", with_panel=True, roster=roster, summary=summary
    )


@app.route("/students")
def students():
    all_students = database.get_students()
    return render_template("students.html", active="students", all_students=all_students)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/attendance")
def attendance():
    return render_template("attendance.html")


@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True)

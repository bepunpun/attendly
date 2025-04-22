from flask import Flask, flash, redirect, render_template, request, url_for

import config
from core import database

app = Flask(__name__)
app.secret_key = "dev"  # fine for a local single-user course project


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        from core.capture import capture_face_samples
        from core.trainer import train_model

        student_id = request.form["student_id"].strip()
        name = request.form["name"].strip()
        program = request.form.get("program", "").strip()

        saved = capture_face_samples(student_id, name, program)
        if saved < 5:
            flash(f"Only captured {saved} samples — try again with better lighting.")
            return redirect(url_for("register"))

        train_model()
        flash(f"{name} registered and model retrained ({saved} samples).")
        return redirect(url_for("students"))

    return render_template(
        "register.html", active="register", samples_per_student=config.SAMPLES_PER_STUDENT
    )


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

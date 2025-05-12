import csv
import io

from flask import Flask, Response, flash, jsonify, redirect, render_template, request, url_for

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
    status_filter = request.args.get("status", "all")
    records = database.get_attendance_history()
    if status_filter != "all":
        records = [r for r in records if r["status"] == status_filter]

    return render_template(
        "attendance.html", active="attendance", records=records, status_filter=status_filter
    )


@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/attendance/export.csv")
def export_attendance_csv():
    records = database.get_attendance_history(limit=5000)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["student_id", "name", "program", "timestamp", "status"])
    for r in records:
        writer.writerow([r["student_id"], r["name"], r["program"], r["timestamp"], r["status"]])

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance.csv"},
    )


@app.route("/api/students/<student_id>")
def api_student_detail(student_id):
    student = database.get_student(student_id)
    if not student:
        return jsonify({"error": "not found"}), 404

    stats = database.get_student_stats(student_id)
    return jsonify(
        {
            "student_id": student["student_id"],
            "name": student["name"],
            "program": student["program"],
            "enrolled": student["created_at"][:10],
            "last_seen": stats["last_seen"],
            "attendance_rate": stats["attendance_rate"],
        }
    )


@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True)

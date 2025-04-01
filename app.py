from flask import Flask, render_template

import config
from core import database

app = Flask(__name__)


@app.before_request
def _ensure_db():
    database.init_db()


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/students")
def students():
    return render_template("students.html")


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

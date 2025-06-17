# RollCall

A lightweight, web-based face recognition attendance system.

Register students from a webcam, train a recognizer on their faces, then
mark attendance automatically as people walk in front of the camera — no
sign-in sheets. Built as a semester project.

## Stack

- **Detection/recognition:** OpenCV Haar cascade + LBPH face recognizer
- **Backend:** Flask, SQLite
- **Frontend:** server-rendered Jinja templates, vanilla JS, gruvbox-themed CSS
- **Reports:** CSV export, optional emailed report via SMTP

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate          # .venv\Scripts\activate on Windows
pip install -r requirements.txt

# optional: populate the dashboard with fake students/attendance
python scripts/seed_demo_data.py

python app.py                      # http://127.0.0.1:5000
```

To register a real student, go to **Register**, enter their ID/name, and
look at the webcam when you submit — RollCall captures face samples and
retrains the recognizer automatically. **Recognize & Attendance** isn't
wired to a live camera route yet; recognition currently runs via
`core.recognizer.recognize_frame()` against a single captured frame.

### Email reports (optional)

Set these before running the app if you want the **Reports** page to be
able to send mail:

```bash
export ROLLCALL_SMTP_USER=you@gmail.com
export ROLLCALL_SMTP_PASSWORD=your-app-password
export ROLLCALL_REPORT_EMAIL=default-recipient@example.com
```

## Project layout

```
app.py                 Flask routes
config.py               paths, camera index, thresholds
core/
  database.py            SQLite schema + queries
  detector.py             Haar cascade wrapper
  capture.py               registration capture flow
  trainer.py                LBPH training
  recognizer.py              recognition + attendance marking
  mailer.py                   SMTP report delivery
  settings_store.py            runtime-editable settings
scripts/
  check_camera.py         webcam sanity check
  seed_demo_data.py       fake data for demoing the UI
templates/, static/     the gruvbox dashboard UI
```

## Status

Core pipeline (capture → train → recognize → log) and the dashboard are
working. Known gaps: no live in-browser camera preview yet, and the
recognizer isn't hooked up to a continuous video loop — see Status above.

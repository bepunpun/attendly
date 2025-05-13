import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def send_report(to_addr: str, csv_bytes: bytes, subject: str = "RollCall attendance report"):
    if not (config.SMTP_USER and config.SMTP_PASSWORD):
        raise RuntimeError("SMTP credentials not configured (see .env)")

    msg = MIMEMultipart()
    msg["From"] = config.SMTP_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText("Attendance report attached.", "plain"))

    attachment = MIMEApplication(csv_bytes, Name="attendance.csv")
    attachment["Content-Disposition"] = 'attachment; filename="attendance.csv"'
    msg.attach(attachment)

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(msg)

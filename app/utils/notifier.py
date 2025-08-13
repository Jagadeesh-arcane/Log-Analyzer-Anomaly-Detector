# src/utils/notifier.py

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
SENDER_NAME = os.getenv("SENDER_NAME", "Log-Analyzer-Testing")
USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("true", "1", "yes")


def send_email_alert(subject, body, to_email=ALERT_EMAIL_TO, dry_run=False):
    if dry_run:
        print(f"✉️ [DRY RUN] Email to {to_email}:\nSubject: {subject}\n\n{body}")
        return

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = f"{SENDER_NAME} <{EMAIL_USER}>"
        msg['To'] = to_email

        if USE_SSL:
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)

        print("✅ Email sent successfully.")

    except Exception as e:
        print(f"❌ Failed to send email ({type(e).__name__}): {e}")

import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")

# Custom sender name
SENDER_NAME = os.getenv("SENDER_NAME", "Log-Analyzer-Testing")  # fallback if not provided

def send_email_alert(subject, body, to_email=ALERT_EMAIL_TO):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = f"{SENDER_NAME} <{EMAIL_USER}>"
        msg['To'] = to_email

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
            print("✅ Email sent successfully.")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

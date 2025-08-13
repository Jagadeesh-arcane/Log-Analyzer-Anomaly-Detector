# app/src/run.py

import sys
import os
from dotenv import load_dotenv
from parser import parse_log_file
from analyzer import get_log_level_counts, get_frequent_errors
from detector import detect_high_response_times
from utils.notifier import send_email_alert
from pprint import pprint

# Setup path and env
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "app/logs/test-1.log")
RESPONSE_TIME_THRESHOLD = int(os.getenv("RESPONSE_TIME_THRESHOLD", 1000))


def main():
    # Check if file exists
    if not os.path.exists(LOG_FILE_PATH):
        print(f"❌ Log file not found: {LOG_FILE_PATH}")
        sys.exit(1)

    print(f"📄 Parsing log file: {LOG_FILE_PATH}")
    logs = parse_log_file(LOG_FILE_PATH)

    if not logs:
        print("⚠️ No logs found or failed to parse.")
        return

    print(f"✅ Parsed {len(logs)} log entries.\n")

    print("📊 Log Level Counts:")
    pprint(get_log_level_counts(logs))

    print("\n🐞 Frequent Errors:")
    frequent_errors = get_frequent_errors(logs)
    if frequent_errors:
        pprint(frequent_errors)
    else:
        print("No errors found.")

    anomalies = detect_high_response_times(logs, RESPONSE_TIME_THRESHOLD)
    if anomalies:
        print(f"\n🚨 Detected {len(anomalies)} high response time logs:")
        for a in anomalies:
            print(f"- {a['timestamp']} | {a['response_time']}ms | {a['message']}")

        # Optional: comment out to disable during debugging
        print("\n📩 Sending email alert...")
        body = "\n".join([f"{a['timestamp']} - {a['message']}" for a in anomalies])
        send_email_alert("🚨 High API Response Time Detected", body)
        print("✅ Email sent.")
    else:
        print("\n✅ No high response time anomalies found.")


if __name__ == "__main__":
    main()

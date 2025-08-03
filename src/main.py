import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from parser import parse_log_file
from analyzer import get_log_level_counts, get_frequent_errors
from detector import detect_high_response_times
from utils.notifier import send_email_alert

load_dotenv()

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/sample.log")
RESPONSE_TIME_THRESHOLD = int(os.getenv("RESPONSE_TIME_THRESHOLD", 1000))

def main():
    logs = parse_log_file(LOG_FILE_PATH)

    print("Log Level Counts:")
    print(get_log_level_counts(logs))

    print("\nFrequent Errors:")
    print(get_frequent_errors(logs))

    anomalies = detect_high_response_times(logs, RESPONSE_TIME_THRESHOLD)
    if anomalies:
        print("\n⚠️ Detected High Response Time Logs:")
        for a in anomalies:
            print(a)

        body = "\n".join([f"{a['timestamp']} - {a['message']}" for a in anomalies])
        send_email_alert("High API Response Time Detected", body)

if __name__ == "__main__":
    main()

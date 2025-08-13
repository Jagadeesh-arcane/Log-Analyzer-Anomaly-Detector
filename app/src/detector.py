# app/src/detector.py

import re

def detect_high_response_times(logs, threshold_ms=1000):
    """
    Detects logs with API response times greater than the given threshold.
    
    Args:
        logs (list): List of log dictionaries.
        threshold_ms (int): Threshold in milliseconds.

    Returns:
        list: List of anomaly dicts with timestamp, response_time, and message.
    """
    anomalies = []
    pattern = re.compile(r"API response time: (\d+)ms", re.IGNORECASE)

    for log in logs:
        message = log.get("message", "")
        timestamp = log.get("timestamp", "")
        match = pattern.search(message)
        if match:
            try:
                response_time = int(match.group(1))
                if response_time > threshold_ms:
                    anomalies.append({
                        "timestamp": timestamp,
                        "response_time": response_time,
                        "message": message
                    })
            except ValueError:
                continue  # Skip malformed response time

    # Optional: sort by response time (descending)
    anomalies.sort(key=lambda x: x["response_time"], reverse=True)
    return anomalies

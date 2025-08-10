def detect_high_response_times(logs, threshold_ms=1000):
    anomalies = []
    for log in logs:
        if "API response time" in log["message"]:
            parts = log["message"].split(":")
            if len(parts) > 1:
                try:
                    response_time = int(parts[1].strip().replace("ms", ""))
                    if response_time > threshold_ms:
                        anomalies.append({
                            "timestamp": log["timestamp"],
                            "response_time": response_time,
                            "message": log["message"]
                        })
                except ValueError:
                    continue
    return anomalies

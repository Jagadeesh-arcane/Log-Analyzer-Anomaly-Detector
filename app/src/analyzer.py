# src/analyzer.py

from collections import Counter

def get_log_level_counts(logs):
    levels = [log["level"] for log in logs]
    return dict(Counter(levels))

def get_frequent_errors(logs):
    errors = [log["message"] for log in logs if log["level"] == "ERROR"]
    return dict(Counter(errors))

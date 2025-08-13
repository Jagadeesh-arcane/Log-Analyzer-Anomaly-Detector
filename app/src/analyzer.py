# app/src/analyzer.py

from collections import Counter

def get_log_level_counts(logs):
    """Count occurrences of each log level."""
    levels = [log.get("level") for log in logs if log.get("level")]
    return dict(Counter(levels).most_common())

def get_frequent_errors(logs, min_count=2):
    """
    Return frequent error messages with a minimum count.
    Args:
        logs (list): List of log dicts.
        min_count (int): Minimum frequency for an error to be returned.
    Returns:
        dict: Error message -> count
    """
    errors = [log.get("message") for log in logs if log.get("level") == "ERROR" and log.get("message")]
    counter = Counter(errors)
    return {msg: count for msg, count in counter.items() if count >= min_count}

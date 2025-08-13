# app/src/parser.py

import re
import json

def parse_log_line(line):
    """
    Attempts to parse a single log line into a dictionary with timestamp, level, and message.
    Supports:
        - JSON logs
        - Space-separated logs: YYYY-MM-DD HH:MM:SS LEVEL Message
        - Dash-separated logs: Timestamp - LEVEL - Message
    Returns:
        dict or None
    """
    line = line.strip()
    if not line:
        return None

    # 1. JSON log format
    try:
        log_obj = json.loads(line)
        return {
            "timestamp": log_obj.get("timestamp", ""),
            "level": log_obj.get("level", "").upper(),
            "message": log_obj.get("message", "")
        }
    except json.JSONDecodeError:
        pass

    # 2. Space-separated logs: 2025-08-13 15:22:01 INFO Some message
    space_pattern = re.match(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)$", line)
    if space_pattern:
        date, time, level, message = space_pattern.groups()
        return {
            "timestamp": f"{date} {time}",
            "level": level.upper(),
            "message": message
        }

    # 3. Dash-separated logs: 2025-08-13 15:22:01 - INFO - Some message
    dash_parts = line.split(" - ")
    if len(dash_parts) == 3:
        timestamp, level, message = dash_parts
        return {
            "timestamp": timestamp.strip(),
            "level": level.strip().upper(),
            "message": message.strip()
        }

    # Fallback: unrecognized format
    return None


def parse_log_file(file, last_n_lines=None):
    """
    Reads and parses a log file into structured log entries.
    Args:
        file: file path or uploaded file-like object
        last_n_lines: limit to last N lines (for tail mode)
    Returns:
        list of parsed log dicts
    """
    # Read lines
    if hasattr(file, "read"):
        try:
            lines = file.read().decode("utf-8").splitlines()
        except Exception:
            lines = file.read().splitlines()  # for strIO
    else:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

    if last_n_lines:
        lines = lines[-last_n_lines:]

    parsed_logs = []
    for line in lines:
        parsed = parse_log_line(line)
        if parsed:
            parsed_logs.append(parsed)

    return parsed_logs

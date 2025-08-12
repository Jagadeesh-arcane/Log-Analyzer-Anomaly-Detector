# src/parser.py

import re
import json

def parse_log_line(line):
    log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)"
    match = re.match(log_pattern, line)
    if match:
        timestamp, level, message = match.groups()
        return {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
    return None

def parse_log_file(file, last_n_lines=None):
    logs = []

    if hasattr(file, "read"):
        lines = file.read().decode("utf-8").splitlines()
    else:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

    if last_n_lines:
        lines = lines[-last_n_lines:]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Try JSON log
        try:
            log_obj = json.loads(line)
            logs.append({
                "timestamp": log_obj.get("timestamp", ""),
                "level": log_obj.get("level", "").upper(),
                "message": log_obj.get("message", "")
            })
            continue
        except json.JSONDecodeError:
            pass

        # Try space-separated logs (e.g., time level message)
        parts = line.split(" ", 2)
        if len(parts) == 3:
            timestamp = f"{parts[0]} {parts[1]}"
            level_msg = parts[2].split(" ", 1)
            if len(level_msg) == 2:
                level = level_msg[0].upper()
                message = level_msg[1]
                logs.append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": message
                })
                continue

        # Try dash-separated logs: timestamp - LEVEL - message
        dash_parts = line.split(" - ")
        if len(dash_parts) == 3:
            logs.append({
                "timestamp": dash_parts[0],
                "level": dash_parts[1].upper(),
                "message": dash_parts[2]
            })

    return logs

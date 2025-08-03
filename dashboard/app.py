import streamlit as st
import os
import sys
import re
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Add import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import parse_log_file
from analyzer import get_log_level_counts, get_frequent_errors
from detector import detect_high_response_times
from utils.notifier import send_email_alert

# Load .env
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
SENDER_NAME = os.getenv("SENDER_NAME", "Log Analyzer")
RESPONSE_TIME_THRESHOLD = int(os.getenv("RESPONSE_TIME_THRESHOLD", 1000))

# Streamlit config
st.set_page_config(
    page_title="Log Analyzer & Anomaly Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Log Analyzer & Anomaly Detector")

# Auto-refresh logic
refresh_interval = st.sidebar.slider("⏱ Auto-refresh interval (sec)", 5, 60, 10)
st_autorefresh = st.sidebar.checkbox("Enable Auto-refresh", value=False)
if st_autorefresh:
    import time
    time.sleep(refresh_interval)
    st.rerun()

# Select from available files or upload
log_files = [f for f in os.listdir("logs") if f.endswith(".log")]
selected_log_file = st.selectbox("📁 Select a log file", log_files)
uploaded_file = st.file_uploader("Or upload your own .log file", type=["log"])

# Parse logs
# Tail mode toggle and slider
tail_mode = st.sidebar.checkbox("🟡 Tail log (show last N lines only)", value=False)
tail_count = st.sidebar.slider("Lines to show", 10, 500, 100) if tail_mode else None

# Parse logs from uploaded file or selected file
if uploaded_file is not None:
    logs = parse_log_file(uploaded_file, last_n_lines=tail_count)
    st.success("✅ Uploaded log file loaded.")
elif selected_log_file:
    file_path = os.path.join("logs", selected_log_file)
    logs = parse_log_file(file_path, last_n_lines=tail_count)
    st.success(f"📄 Loaded log file: `{selected_log_file}`")
else:
    logs = []


# Enhanced UI: filters and view modes
st.sidebar.header("🔍 Filter Logs")

view_mode = st.sidebar.radio("View Mode", ["Simple View", "Advanced View"])
log_levels = list(set(log["level"] for log in logs))
selected_levels = st.sidebar.multiselect("Log Levels", log_levels, default=log_levels)

search_term = st.sidebar.text_input("Search keyword (In-logs)")

# Time range filtering
timestamps = [datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S") for log in logs if log["timestamp"]]
if timestamps:
    min_time, max_time = min(timestamps), max(timestamps)
    if min_time < max_time:
        start_time, end_time = st.sidebar.slider("Time range", min_value=min_time, max_value=max_time, value=(min_time, max_time))
    else:
        start_time = end_time = min_time
        st.sidebar.info(f"Only one timestamp: {min_time}")
else:
    start_time, end_time = None, None

# Filter logs
filtered_logs = []
for log in logs:
    try:
        log_time = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
    except:
        continue
    if start_time and end_time and log["level"] in selected_levels and start_time <= log_time <= end_time:
        if not search_term or search_term.lower() in log["message"].lower():
            filtered_logs.append(log)
df_logs = pd.DataFrame(filtered_logs)
st.download_button("⬇️ Export filtered logs as CSV", df_logs.to_csv(index=False), "filtered_logs.csv", "text/csv")

# Raw preview for simple view
if view_mode == "Simple View":
    st.subheader("📜 Raw Log Preview")
    for log in filtered_logs:
        st.markdown(f"`{log['timestamp']}` | **{log['level']}** — {log['message']}")
    st.stop()

# Response time trend extraction
def extract_response_times(logs):
    data = []
    pattern = re.compile(r'API response time: (\d+)ms')
    for log in logs:
        match = pattern.search(log['message'])
        if match:
            data.append({
                "timestamp": log["timestamp"],
                "response_time": int(match.group(1))
            })
    return pd.DataFrame(data)

if not filtered_logs:
    st.warning("No logs to process.")
    st.stop()

# API Response Time Trend
response_df = extract_response_times(logs)
if not response_df.empty:
    st.subheader("📈 API Response Time Trend")
    st.line_chart(response_df.set_index("timestamp"))

# Log level analysis
st.subheader("🧮 Log Level Breakdown")
level_counts = get_log_level_counts(logs)
st.bar_chart(level_counts)

# Frequent errors
st.subheader("🐞 Frequent Error Messages")
errors = get_frequent_errors(logs)
if errors:
    for err in errors:
        st.write(f"• {err}")
else:
    st.info("No error messages found.")

# Define path for bookmark file
BOOKMARK_FILE = "data/bookmarks.txt"
os.makedirs("data", exist_ok=True)

# Bookmark errors
st.subheader("📌 Bookmark an Error Message")
bookmark = st.selectbox("Choose an error to bookmark", errors)
if st.button("🔖 Save Bookmark"):
    with open(BOOKMARK_FILE, "a") as f:
        f.write(bookmark + "\n")
    st.success("Saved to bookmarks.txt")

# View bookmarks in sidebar
if os.path.exists(BOOKMARK_FILE):
    with open(BOOKMARK_FILE, "r") as f:
        bookmarks = f.read().splitlines()
    if bookmarks:
        st.sidebar.subheader("🔖 Saved Bookmarks")
        for bm in bookmarks:
            st.sidebar.write("-", bm)
        st.sidebar.download_button("⬇️ Download Bookmarks", data="\n".join(bookmarks), file_name="bookmarks.txt")
        if st.sidebar.button("🗑️ Clear Bookmarks"):
            os.remove(BOOKMARK_FILE)
            st.rerun()

# Anomalies
st.subheader("🚨 Response Time Anomalies")
anomalies = detect_high_response_times(logs, RESPONSE_TIME_THRESHOLD)
if anomalies:
    df = pd.DataFrame(anomalies)
    st.dataframe(df, use_container_width=True)

    if st.button("📩 Send Email Alert"):
        body = "\n".join([f"{a['timestamp']} - {a['message']}" for a in anomalies])
        send_email_alert("🚨 High API Response Time Detected", body)
        st.success(f"Alert sent to {ALERT_EMAIL_TO}")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Anomalies CSV", data=csv, file_name="anomalies.csv", mime="text/csv")
else:
    st.info("✅ No high response time anomalies found.")

# Markdown report generation
if st.button("📝 Generate Markdown Summary Report"):
    report = f"# Log Analysis Summary\n\n"
    report += f"**Log File**: {selected_log_file or uploaded_file.name}\n"
    report += f"**Generated**: {datetime.now()}\n\n"
    report += "## Log Level Counts\n"
    for level, count in level_counts.items():
        report += f"- {level}: {count}\n"
    report += "\n## Frequent Errors\n"
    if errors:
        for err in errors:
            report += f"- {err}\n"
    else:
        report += "No errors found.\n"
    report += "\n## Anomalies\n"
    if anomalies:
        for a in anomalies:
            report += f"- {a['timestamp']} — {a['message']}\n"
    else:
        report += "No anomalies found.\n"

    st.download_button(
        label="⬇️ Download Markdown Report",
        data=report,
        file_name="log_summary.md",
        mime="text/markdown"
    )

# Test email button
st.sidebar.header("📧 Email Test")
if st.sidebar.button("Send Test Email"):
    try:
        send_email_alert("✅ Test Email from Log Analyzer", "This is a test email from your Streamlit app.")
        st.sidebar.success("Test email sent!")
    except Exception as e:
        st.sidebar.error(f"Failed: {e}")

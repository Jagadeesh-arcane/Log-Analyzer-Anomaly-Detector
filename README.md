# 📊 Log Analyzer & Anomaly Detector

A powerful and user-friendly **Streamlit** web application to analyze server log files, detect anomalies, visualize trends, and generate reports.  
Designed for **IT infrastructure teams** to monitor backend logs and improve incident response time.

---

## 🧰 Features

- 📂 Upload `.log` files or select from saved logs
- 📈 API response time trends
- 🟡 Real-time log tailing with auto-refresh
- 🧮 Log level breakdown (INFO, WARN, ERROR)
- 🔍 Search & filter logs by level, time, keyword
- 🐞 View most frequent error messages
- 🚨 Anomaly detection (e.g., API latency > 1000ms)
- 📩 Email alerts on anomaly detection
- 🔖 Bookmark important logs
- ⬇️ Download filtered logs as CSV
- 📝 Generate Markdown summary reports
- 🌙 Dark mode ready
- 📡 Deployable via Streamlit Cloud, AWS, or local server

---

## 📁 Project Structure

```
log-analyzer/
├── dashboard/
│   └── app.py                # Main Streamlit UI
├── logs/                     # Place your log files here
├── src/
│   ├── parser.py             # Log parsing logic
│   ├── analyzer.py           # Log analysis (errors, levels)
│   ├── detector.py           # Anomaly detection
│   └── utils/
│       └── notifier.py       # Email alert logic
├── terraform/                # IaC for AWS deployment
├── .env                      # Secure credentials
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🏁 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/log-analyzer.git
cd log-analyzer
```

### 2️⃣ Set Up a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root folder with your configuration:

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ALERT_EMAIL_TO=receiver@example.com
RESPONSE_TIME_THRESHOLD=1000
SENDER_NAME=Log Analyzer
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
ECR_REPOSITORY=your-ecr-repo-name
```

---

## 🚀 Running the Application Locally

```bash
streamlit run dashboard/app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Demo Log File

You can test the app with a sample log file containing 100+ entries across multiple dates.  
Place it in the `logs/` folder and select it via the app UI.

---

## 📦 Deployment

### Streamlit Cloud

1. Push your code to GitHub or GitLab.
2. Link your repo in [Streamlit Community Cloud](https://streamlit.io/cloud).

### AWS Free Tier (via GitLab CI/CD + Terraform)

* Uses `.gitlab-ci.yml` to build a Docker image, push to AWS ECR, and deploy infrastructure via Terraform.

---

## 🙌 Contributing

Contributions are welcome!  
Please open an issue or submit a pull request for new features, bug fixes, or improvements.

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

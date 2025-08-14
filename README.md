
---

# 📊 Log Analyzer & Anomaly Detector — Fully Automated AWS Deployment 🚀

A powerful, fully automated **Streamlit** web application for analyzing server logs, detecting anomalies, visualizing trends, and generating reports.
Now equipped with a **GitLab CI/CD pipeline** that **provisions all required AWS resources**, deploys the app to ECS, and **completely destroys infrastructure** when no longer needed.

---

## 🧰 Features

* 📂 Upload `.log` files or select from saved logs
* 📈 API response time trends
* 🟡 Real-time log tailing with auto-refresh
* 🧮 Log level breakdown (INFO, WARN, ERROR)
* 🔍 Search & filter logs by level, time, keyword
* 🐞 View most frequent error messages
* 🚨 Anomaly detection (e.g., API latency > threshold)
* 📩 Email alerts on anomaly detection
* 🔖 Bookmark important logs
* ⬇️ Download filtered logs as CSV
* 📝 Generate Markdown summary reports
* 🌙 Dark mode ready
* ⚙️ **Fully automated AWS deployment with Terraform**
* 🗑 **One-click infrastructure destroy** (S3, DynamoDB, ECS, etc.)
* 🐳 Automated Docker image build & push to AWS ECR

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
├── .gitlab-ci.yml            # Automated pipeline for build, deploy, destroy
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

Create a `.env` file in the root folder with:

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ALERT_EMAIL_TO=receiver@example.com
RESPONSE_TIME_THRESHOLD=1000
SENDER_NAME=Log Analyzer
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
PROJECT_NAME=log-analyzer
TF_STATE_BUCKET=your-tf-state-bucket
TF_STATE_KEY=terraform.tfstate
TF_STATE_LOCK_TABLE=terraform-lock-table
STREAMLIT_PORT=8501
```

---

## 🚀 Running Locally

```bash
streamlit run dashboard/app.py
```

Then visit:
[http://localhost:8501](http://localhost:8501)

---

## ⚡ Automated AWS Deployment via GitLab CI/CD

This project’s `.gitlab-ci.yml` automates **the entire infrastructure lifecycle**:

1. **Lint** — Validates Terraform code.
2. **Setup** — Creates S3 bucket (for state) and DynamoDB table (for locking).
3. **Backend Init** — Configures Terraform backend.
4. **Infra Plan** — Generates Terraform plan with all variables.
5. **Infra Apply** — Provisions ECS, ECR, ALB, IAM, and networking.
6. **Build Image** — Builds Docker image and pushes to AWS ECR.
7. **Deploy** — Updates ECS service with the new image.
8. **Destroy** *(manual)* — Destroys all AWS resources, including:

   * ECS Service & Cluster
   * ECR Repository Images
   * S3 Bucket & Object Versions
   * DynamoDB Lock Table
   * Networking Components (VPC, Subnets, etc.)

**Triggering Deploy:**

* Push to the `main` branch to deploy automatically.

**Triggering Destroy:**

* Manually run the `destroy` job from GitLab’s CI/CD pipeline UI.

---

## 🧪 Testing

You can use the provided `sample.log` file in `logs/` to simulate real data.

---

## 🙌 Contributing

Contributions are welcome!
Fork the repo, create a feature branch, and submit a PR.

---

## 📜 License

MIT License — see the [LICENSE](LICENSE) file.

---

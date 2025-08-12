# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# reduce pip output and cache
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# entry: run streamlit app (path to your entry file; adjust if inside 'dashboard/app.py')
ENTRYPOINT ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

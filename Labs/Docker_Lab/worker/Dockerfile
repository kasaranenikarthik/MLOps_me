FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r worker && useradd -r -g worker worker

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker.py .

USER worker

CMD ["python", "worker.py"]
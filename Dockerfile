FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/sessions && chmod 777 /app/sessions

ENV SESSION_DIR=/app/sessions

CMD ["python", "-u", "main.py"]

FROM python:3.11-slim

WORKDIR /tmp

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /tmp/

CMD ["python", "-u", "/tmp/main.py"]

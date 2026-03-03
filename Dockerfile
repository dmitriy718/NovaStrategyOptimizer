FROM python:3.11-slim-bookworm

RUN apt-get update -qq && apt-get install -y --no-install-recommends cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]

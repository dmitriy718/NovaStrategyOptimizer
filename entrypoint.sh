#!/bin/bash
set -e
CRON_TIME="${CRON_TIME:-0 2 * * *}"
LOG_FILE=/app/logs/cron.log

# ensure dirs
mkdir -p /app/logs /app/data /app/reports

# write cron job
cat > /etc/cron.d/optimizer <<CRON
${CRON_TIME} root cd /app && /usr/local/bin/python /app/run_once.py >> ${LOG_FILE} 2>&1
CRON
chmod 0644 /etc/cron.d/optimizer
crontab /etc/cron.d/optimizer

# start cron
service cron start

# optional immediate run
echo "Starting optimizer container..."
if [ "${RUN_ON_START}" = "true" ]; then
  python /app/run_once.py
fi
# tail logs to keep container alive
touch ${LOG_FILE}
tail -F ${LOG_FILE}

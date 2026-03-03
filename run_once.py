import os
from datetime import datetime

from engine.optimizer import optimize

DATA_FILE = os.getenv("DATA_FILE", "/app/data/sample_ohlcv.csv")
BASE_CAPITAL = float(os.getenv("BASE_CAPITAL", 10000))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 0)) or None

OUTPUT_DIR = "/app/data"

if __name__ == "__main__":
    start = datetime.utcnow()
    json_path, report_path = optimize(DATA_FILE, BASE_CAPITAL, OUTPUT_DIR, MAX_WORKERS)
    duration = (datetime.utcnow() - start).total_seconds()
    print(f"Optimization complete in {duration:.2f}s")
    print(f"JSON: {json_path}")
    print(f"Report: {report_path}")

import schedule
import time
import subprocess
import sys
from datetime import datetime


def run_ingest():
    print(f"[{datetime.now()}] Running scheduled ingestion...")
    result = subprocess.run(
        [sys.executable, "ingest.py"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"ERROR: {result.stderr}")


# Run immediately on start
run_ingest()

# Then every hour
schedule.every(1).hours.do(run_ingest)

print(f"[{datetime.now()}] Scheduler running — ingesting every hour. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(60)
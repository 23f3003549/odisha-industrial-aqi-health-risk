import schedule
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collect_all_data import collect_owm, collect_waqi
from data_manager import merge_all_snapshots

def job():
    print(f"\nRunning collection job...")
    collect_owm()
    collect_waqi()
    merge_all_snapshots("owm")
    merge_all_snapshots("waqi")
    print("Job done. Next run in 1 hour.")

# Run every 1 hour
schedule.every(1).hours.do(job)

# Run once immediately
job()

print("Scheduler running... keep this terminal open")
while True:
    schedule.run_pending()
    time.sleep(60)
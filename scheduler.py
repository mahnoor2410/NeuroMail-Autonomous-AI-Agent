import schedule
import time
from main_agent import run_once

def job():
    print("\n⏰ Agent running...")
    run_once(max_emails=5, unread_only=True)

if __name__ == "__main__":
    # Run every 5 minutes (for testing set 1 minute)
    schedule.every(5).minutes.do(job)
    print("Scheduler started. Press Ctrl+C to stop.")
    # run one immediately
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

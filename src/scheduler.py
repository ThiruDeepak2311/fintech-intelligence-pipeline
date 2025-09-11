import schedule
import time
import os
from datetime import datetime
from main import FintechPipeline

def run_scheduled_pipeline():
    """Run the pipeline at scheduled time"""
    print(f"🕒 Scheduled run triggered at {datetime.now()}")
    pipeline = FintechPipeline()
    pipeline.run_daily_pipeline()

def start_scheduler():
    """Start the daily scheduler"""
    run_hour = int(os.getenv('RUN_HOUR', 9))  # 9 AM EST
    schedule.every().day.at(f"{run_hour:02d}:00").do(run_scheduled_pipeline)
    
    print(f"📅 Scheduler started - will run daily at {run_hour}:00 EST")
    
    # Run once immediately for demo
    run_scheduled_pipeline()
    
    # Then wait for scheduled times
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    start_scheduler()
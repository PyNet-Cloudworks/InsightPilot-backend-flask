import os
import csv
from datetime import datetime

def log_task(filename, filetype, status, message=""):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # This should create the folder if missing
    log_file = os.path.join(log_dir, "task_log.csv")

    with open(log_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename, filetype, status, message])


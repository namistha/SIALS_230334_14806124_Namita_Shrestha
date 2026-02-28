# collect_today_logs.py
import os
from main import add_log

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Collect today's system logs (requires systemd-journal group or sudo)
os.system("journalctl --since today -o short-iso > logs/today.log")

# Read the log file
with open("logs/today.log", "r") as f:
    log_data = f.read()

# Add logs to the database
add_log(log_data)

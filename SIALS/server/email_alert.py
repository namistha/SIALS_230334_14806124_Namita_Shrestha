from datetime import datetime
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALERT_FILE = os.path.join(BASE_DIR, "alerts.log")

def send_tamper_alert():

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"{timestamp} | ALERT: Log Tampering Detected - Integrity Verification Failed\n"

    with open(ALERT_FILE, "a") as f:
        f.write(message)

    print("ALERT LOGGED:", message)


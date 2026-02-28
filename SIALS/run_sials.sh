#!/bin/bash

# -------------------------------
# Secure Incident Audit Logging System
# Cron-ready execution script
# -------------------------------

# 1️⃣ Activate your Python virtual environment
source /home/namita/SIALS/crypto_env/bin/activate

# 2️⃣ Navigate to project folder
cd /home/namita/SIALS || exit 1

# 3️⃣ Run your main Python script
# All output (stdout + stderr) goes to cron.log
python main.py >> logs/cron.log 2>&1

# 4️⃣ Optional: add a timestamp in cron.log for reference
echo "✅ Run completed at $(date)" >> logs/cron.log


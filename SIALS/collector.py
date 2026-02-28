import subprocess
import zipfile
from datetime import datetime
from main import add_log

today = datetime.now().strftime("%Y-%m-%d")
filename = f"logs_{today}.txt"
zipname = f"logs_{today}.zip"

# collect system logs
logs = subprocess.check_output(
    ["journalctl", "--since", "today"],
    text=True
)

# save raw
with open(filename, "w") as f:
    f.write(logs)

# add each line as DB log
for line in logs.splitlines():
    if line.strip():
        add_log(line)

# zip archive
with zipfile.ZipFile(zipname, "w") as z:
    z.write(filename)

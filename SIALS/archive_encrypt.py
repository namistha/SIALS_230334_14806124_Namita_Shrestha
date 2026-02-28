import zipfile
from datetime import datetime
import os
from crypto.aes_encrypt import encrypt_file

DATE = datetime.now().strftime("%Y-%m-%d")

DB_FILE = "db/logs.db"
STORAGE_DIR = "storage"

ZIP_NAME = f"{STORAGE_DIR}/logs_{DATE}.zip"

print("[+] Creating ZIP archive...")

with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(DB_FILE)

print("✔ ZIP created:", ZIP_NAME)

print("[+] Encrypting ZIP using AES...")

encrypted_file = encrypt_file(ZIP_NAME)

print("✔ AES encryption completed")

print("[+] Deleting plaintext ZIP...")

os.remove(ZIP_NAME)

print("✔ Plain ZIP deleted (secure storage mode)")


import hashlib
import sqlite3
from datetime import datetime
from crypto.aes_encrypt import encrypt_log
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "db", "logs.db")


# -----------------------------
# HASH GENERATOR (CHAINED)
# -----------------------------

def generate_hash(log_data, previous_hash):
    data = log_data + previous_hash
    return hashlib.sha256(data.encode()).hexdigest()


# -----------------------------
# ADD LOG ENTRY
# -----------------------------

def add_log(log_data):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT hash FROM logs ORDER BY id DESC LIMIT 1")
    last = cursor.fetchone()

    prev_hash = last[0] if last else ""

    encrypted_log = encrypt_log(log_data)

    new_hash = generate_hash(encrypted_log, prev_hash)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO logs (log_data, hash, prev_hash, timestamp) VALUES (?, ?, ?, ?)",
        (encrypted_log, new_hash, prev_hash, timestamp)
    )

    conn.commit()
    conn.close()

    print("✔ Log Added Securely")


# -----------------------------
# VERIFY LOG CHAIN (TAMPER DETECTION)
# -----------------------------

def verify_chain(return_index=False):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT id, log_data, hash, prev_hash FROM logs ORDER BY id")
    rows = cursor.fetchall()

    prev_hash = ""

    for i, row in enumerate(rows):

        log_data = row[1]
        stored_hash = row[2]
        db_prev_hash = row[3]

        recalculated = generate_hash(log_data, prev_hash)

        if stored_hash != recalculated or db_prev_hash != prev_hash:

            conn.close()

            if return_index:
                return False, i
            else:
                return False

        prev_hash = stored_hash

    conn.close()

    if return_index:
        return True, None

    return True


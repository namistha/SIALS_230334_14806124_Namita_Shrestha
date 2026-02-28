import sys
import os
import sqlite3
import csv
import datetime
import io

from flask import Flask, render_template, request, redirect, session, send_file

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(BASE_DIR, "../db/logs.db")
ALERT_FILE = os.path.join(BASE_DIR, "alerts.log")

sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, "..")))

from main import verify_chain
from server.email_alert import send_tamper_alert
from crypto.aes_encrypt import decrypt_log

app = Flask(__name__)
app.secret_key = "sials_secret_key"

# Prevent alert spam
ALERT_SENT = False

# -------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------
def get_db():
    # timeout=10 allows SQLite to wait 10 seconds if DB is locked
    conn = sqlite3.connect(DB, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------------------------
# SYSTEM STATS
# -------------------------------------------------
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM logs
        WHERE DATE(timestamp)=DATE('now','localtime')
    """)
    total_logs = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM logs
        WHERE is_tampered=1
        AND DATE(timestamp)=DATE('now','localtime')
    """)
    tampered_logs = cursor.fetchone()[0]

    verified_logs = total_logs - tampered_logs
    conn.close()
    return total_logs, verified_logs, tampered_logs

# -------------------------------------------------
# GRAPH ANALYTICS
# -------------------------------------------------
def get_log_graph():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(timestamp,'localtime') as day, COUNT(*) as count
        FROM logs
        GROUP BY day
        ORDER BY day DESC
        LIMIT 14
    """)

    rows = cursor.fetchall()
    conn.close()

    labels = [row["day"] for row in rows]
    counts = [row["count"] for row in rows]

    return labels, counts

# -------------------------------------------------
# ALERT LOGGING
# -------------------------------------------------
def log_alert(msg):
    with open(ALERT_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} : {msg}\n")

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username, role FROM users WHERE username=? AND password=?",
            (user, pwd)
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            if result["role"] != "admin":
                return render_template("login.html", error="⛔ Privilege Not Allowed")

            session["user"] = result["username"]
            session["role"] = result["role"]

            return redirect("/")

        return render_template("login.html", error="❌ Invalid Username or Password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
@app.route("/")
def dashboard():
    global ALERT_SENT
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, log_data, hash, is_tampered
        FROM logs
        WHERE DATE(timestamp)=DATE('now','localtime')
        ORDER BY id DESC
        LIMIT 50
    """)
    logs = cursor.fetchall()
    conn.close()

    graph_labels, graph_counts = get_log_graph()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM logs
        WHERE is_tampered=1
        AND DATE(timestamp)=DATE('now','localtime')
    """)
    tampered_logs = cursor.fetchone()[0]
    conn.close()

    if tampered_logs > 0 and not ALERT_SENT:
        send_tamper_alert()
        log_alert("🚨 Today's Logs Tampered")
        ALERT_SENT = True

    total_logs, verified_logs, _ = get_stats()

    return render_template(
        "dashboard.html",
        logs=logs,
        total_logs=total_logs,
        verified_logs=verified_logs,
        tampered_logs=tampered_logs,
        graph_labels=graph_labels,
        graph_counts=graph_counts,
        user=session["user"]
    )

# -------------------------------------------------
# LOGS PAGE
# -------------------------------------------------
@app.route("/logs")
def view_logs():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, log_data, hash, is_tampered
        FROM logs
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    logs = []
    for r in rows:
        try:
            data = decrypt_log(r["log_data"])
        except:
            data = r["log_data"]

        logs.append({
    "timestamp": r["timestamp"],
    "log_data": data,
    "hash": r["hash"],
    "is_tampered": r["is_tampered"],
    "is_encrypted": isinstance(r["log_data"], str) and r["log_data"].startswith("gAAAA")
    })
    total_logs, verified_logs, tampered_logs = get_stats()

    return render_template(
        "logs.html",
        logs=logs,
        total_logs=total_logs,
        verified_logs=verified_logs,
        tampered_logs=tampered_logs,
        user=session["user"]
    )

# -------------------------------------------------
# ALERTS PAGE
# -------------------------------------------------
@app.route("/alerts")
def alerts():
    if "user" not in session:
        return redirect("/login")

    alerts = []
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE) as f:
            alerts = f.readlines()

    total_logs, verified_logs, tampered_logs = get_stats()

    return render_template(
        "alerts.html",
        alerts=alerts,
        total_logs=total_logs,
        verified_logs=verified_logs,
        tampered_logs=tampered_logs,
        user=session["user"]
    )

# -------------------------------------------------
# SETTINGS PAGE
# -------------------------------------------------
@app.route("/settings")
def settings():
    if "user" not in session:
        return redirect("/login")

    total_logs, verified_logs, tampered_logs = get_stats()

    return render_template(
        "settings.html",
        total_logs=total_logs,
        verified_logs=verified_logs,
        tampered_logs=tampered_logs,
        user=session["user"]
    )

# -------------------------------------------------
# EXPORT LOGS PAGE (button page)
# -------------------------------------------------
@app.route("/export_logs_page")
def export_logs_page():
    if "user" not in session:
        return redirect("/login")

    total_logs, verified_logs, tampered_logs = get_stats()

    return render_template(
        "export_logs.html",
        total_logs=total_logs,
        verified_logs=verified_logs,
        tampered_logs=tampered_logs,
        user=session["user"]
    )

# -------------------------------------------------
# EXPORT LOGS DOWNLOAD (memory-safe CSV)
# -------------------------------------------------
@app.route("/export_logs_download")
def export_logs_download():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, log_data, hash, is_tampered FROM logs")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "Log Data", "Hash", "Tampered"])

    for r in rows:
        data = r["log_data"]
        if isinstance(data, str) and data.startswith("gAAAA"):
            try:
                data = decrypt_log(data)
            except:
                data = "[Encrypted — Cannot Decrypt]"

        writer.writerow([r["timestamp"], data, r["hash"], r["is_tampered"]])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="export_logs.csv"
    )

# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

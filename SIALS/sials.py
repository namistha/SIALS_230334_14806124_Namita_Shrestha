import sys
from main import add_log, verify_chain

def show_help():
    print("""
SIALS - Secure Incident Audit Logging System

Usage:
  sials --log "message"     Add secure log
  sials --verify            Verify log integrity
  sials --status            System status
""")

if len(sys.argv) < 2:
    show_help()
    exit()

cmd = sys.argv[1]

if cmd == "--log":
    message = sys.argv[2]
    add_log(message)

elif cmd == "--verify":
    verify_chain()

elif cmd == "--status":
    print("SIALS running normally ✔")

else:
    show_help()


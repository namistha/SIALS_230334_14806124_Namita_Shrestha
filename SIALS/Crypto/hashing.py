import hashlib

def generate_hash(log, prev_hash=""):
    combined = log + prev_hash
    return hashlib.sha256(combined.encode()).hexdigest()






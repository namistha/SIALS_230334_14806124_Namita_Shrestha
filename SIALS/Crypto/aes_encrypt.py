from cryptography.fernet import Fernet
import os

KEY_FILE = "keys/aes.key"

# Create AES key only once
if not os.path.exists(KEY_FILE):
    os.makedirs("keys", exist_ok=True)
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

# -----------------------------
# Encrypt a string (log data)
# -----------------------------
def encrypt_log(data_str):
    # Read the key
    with open(KEY_FILE, "rb") as f:
        key = f.read()

    fernet = Fernet(key)

    # Encrypt the string (convert to bytes first)
    encrypted_data = fernet.encrypt(data_str.encode())

    # Return as string (decode to store in DB)
    return encrypted_data.decode()


# Optional: Decrypt function for later use
def decrypt_log(encrypted_str):
    with open(KEY_FILE, "rb") as f:
        key = f.read()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_str.encode())
    return decrypted_data.decode()

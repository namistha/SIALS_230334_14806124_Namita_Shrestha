# Secure Incident Audit Logging System (SIALS)

Secure Incident Audit Logging System (SIALS) is a Python-based tool that provides secure, tamper-proof logging of system and user events. It uses SHA-256 hashing, ECDSA digital signatures, and AES encryption to ensure **confidentiality, integrity, authentication, and tamper-proof audit logs**.

---

## Description

Secure Incident Audit Logging System (SIALS) captures system and user events, securing them with SHA-256 hashing, ECDSA digital signatures, and AES encryption. Logs are chained to prevent tampering, verified for integrity, and stored securely, providing reliable, tamper-proof audit logging for educational purposes.

---

## Features

- Digital Signatures (ECDSA) for tamper-proof logs  
- Hash Chaining using SHA-256 for integrity  
- AES encryption for secure log storage  
- Secure key management with password-protected keystore  
- Log verification and tamper detection  
- Optional reporting in CSV/JSON format  
- CLI interface for capturing and verifying logs  

---

## Technologies Used

- Python 3.x  
- Flask (optional web interface)  
- SQLite for log storage  
- `cryptography` for encryption and digital signatures  
- `hashlib` for hashing  
- `pytest` for unit testing  

---

## Installation

1. Clone the repository:  
```bash
git clone https://github.com/your-username/sials.git
cd sials

Install required packages:

pip install -r requirements.txt

Run the tool:

python sials.py
Usage

Start the tool and input system or user event data.

Logs are hashed, signed, and encrypted automatically.

Encrypted logs are stored securely in SQLite.

To verify logs:

Decrypt logs

Verify digital signatures

Validate hash chain integrity

Optionally, save verification reports in CSV or JSON format.

Use Cases

Secure audit logging for system events

Prevent tampering during educational demonstrations of logging

Demonstrating cryptographic integrity and authentication concepts

Testing

Unit tests implemented using pytest

Tests include log creation, signature verification, hash chain validation, and tamper detection

Run tests using:

pytest
License

This project is created solely for educational purposes. It demonstrates secure audit logging, digital signatures, hash chaining, and encryption techniques. It is not intended for commercial use or production deployment.

Author

Namita Shrestha

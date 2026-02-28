Secure Incident Audit Logging System (SIALS)

Secure Incident Audit Logging System (SIALS) is a Python-based tool designed to provide secure, tamper-proof logging of system and user events. It uses SHA-256 hashing, ECDSA digital signatures, and AES encryption to ensure confidentiality, integrity, authentication, and tamper-proof audit logs.

Description

SIALS captures system and user events, securing them with SHA-256 hashing, ECDSA digital signatures, and AES encryption. Logs are chained to prevent tampering, verified for integrity, and stored securely, providing reliable, tamper-proof audit logging for educational purposes.

Features

Digital Signatures (ECDSA) for tamper-proof logs

Hash Chaining using SHA-256 for integrity

AES Encryption for secure log storage

Secure key management with password-protected keystore

Log verification and tamper detection

Optional reporting in CSV/JSON format

CLI interface for capturing and verifying logs

Technologies Used

Python 3.x

Flask (optional web interface)

SQLite (database for storing logs)

cryptography library for encryption and digital signatures

hashlib for hashing logs

pytest for unit testing

Installation
1. Clone the Repository
git clone https://github.com/your-username/sials.git
cd sials
2. Install Required Packages
pip install -r requirements.txt
3. Run the Tool
python sials.py
Usage

Start the tool and input system or user event data.

Logs are hashed, digitally signed, and encrypted automatically.

Encrypted logs are securely stored in SQLite.

For verification: decrypt logs, verify digital signatures, and check hash chain integrity.

Optionally, generate and save a report in CSV or JSON format.

Use Cases

Secure logging of system and user events for educational demonstrations

Prevent tampering while teaching cryptographic integrity and authentication concepts

Demonstrate audit logging processes and verification techniques

Testing

Unit tests implemented using pytest.

Test cases include:

Log creation

Signature verification

Hash chain validation

Tamper detection

Run tests using:

pytest
License

This project is created solely for educational purposes. It demonstrates secure audit logging, digital signatures, hash chaining, and encryption techniques. It is not intended for commercial use or production deployment.

Author

Namita Shrestha

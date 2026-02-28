# Secure Incident Audit Logging System (SIALS)

Secure Incident Audit Logging System (SIALS) is a Python-based tool designed to provide secure, tamper-proof logging of system and user events. It uses SHA-256 hashing, ECDSA digital signatures, and AES encryption to ensure **confidentiality, integrity, authentication, and tamper-proof audit logs**.

---

## Description

SIALS captures system and user events, securing them with SHA-256 hashing, ECDSA digital signatures, and AES encryption. Logs are chained to prevent tampering, verified for integrity, and stored securely, providing reliable, tamper-proof audit logging for **educational purposes**.

---

## Features

- **Digital Signatures**: Each log entry is signed using ECDSA to prevent tampering.  
- **Hash Chaining**: Logs are linked using SHA-256 to detect unauthorized modifications.  
- **AES Encryption**: Logs are encrypted using AES-256 for secure storage.  
- **Secure Key Management**: Private keys stored in password-protected keystore.  
- **Log Verification**: Decrypt and verify log integrity and signatures.  
- **Tamper Detection & Alerts**: Detect and alert on unauthorized log modifications.  
- **Reporting**: Optionally save logs and verification results in CSV or JSON format.  
- **CLI Interface**: Easy command-line interface for capturing and verifying logs.  

---

## Technologies Used

- **Python 3.x**  
- **Flask** (optional web interface)  
- **SQLite** (lightweight database for storing logs)  
- **cryptography** library for encryption and digital signatures  
- **hashlib** for hashing logs  
- **pytest** for unit testing  

---

## Installation

1. Clone the repository:  
```bash
git clone https://github.com/your-username/sials.git
cd sials

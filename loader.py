#!/usr/bin/env python3
import getpass
import os
from pathlib import Path
import subprocess

# Path to encrypted file
ENC_FILE = Path("mysc.py.enc")

if not ENC_FILE.exists():
    print("Encrypted file not found:", ENC_FILE)
    exit(1)

# Ask password
password = getpass.getpass("Enter password: ")

# Decrypt using OpenSSL into memory (stdout)
try:
    result = subprocess.run(
        ["openssl", "enc", "-aes-256-cbc", "-d", "-pbkdf2", "-salt",
         "-in", str(ENC_FILE), "-pass", "pass:" + password],
        capture_output=True
    )
except FileNotFoundError:
    print("OpenSSL not found. Install it: pkg install openssl")
    exit(1)

if result.returncode != 0:
    print("Decryption failed. Wrong password or corrupted file.")
    exit(1)

# Decrypted code in memory
code = result.stdout.decode("utf-8")

# Execute decrypted code
exec(code)

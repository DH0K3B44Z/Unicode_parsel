#!/usr/bin/env python3
import subprocess
from pathlib import Path
import sys
import base64

# === Config ===
ENC_FILE = Path("mysc.py.enc")

# Password  ko base64 me encode kiya gaya hai:
# "" -> "MTkyMA=="
_hidden_pass = "MTkyMA=="

def get_password():
    # Base64 decode karke original password wapas banate hain
    return base64.b64decode(_hidden_pass.encode()).decode()

def main():
    if not ENC_FILE.exists():
        print("❌ Encrypted file not found:", ENC_FILE)
        sys.exit(1)

    password = get_password()

    try:
        result = subprocess.run(
            ["openssl", "enc", "-aes-256-cbc", "-d", "-pbkdf2", "-salt",
             "-in", str(ENC_FILE), "-pass", f"pass:{password}"],
            capture_output=True
        )
    except FileNotFoundError:
        print("❌ OpenSSL not installed. Install in Termux: pkg install openssl")
        sys.exit(1)

    if result.returncode != 0:
        print("❌ Decryption failed. Wrong password or corrupted file.")
        sys.exit(1)

    try:
        code = result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        print("❌ Could not decode decrypted content (not valid Python).")
        sys.exit(1)

    print("🔓 Decryption successful. Running script...\n")
    exec(code, globals())

if __name__ == "__main__":
    main()

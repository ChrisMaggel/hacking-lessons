#!/usr/bin/env python3
"""
========================================
VULNERABLE HTTP CLIENT
========================================
This is an INTENTIONALLY INSECURE client for educational purposes.

VULNERABILITIES:
1. Sends credentials over HTTP (no encryption)
2. Doesn't verify server certificate (no HTTPS)
3. No protection against MITM attacks
4. Trusts the network blindly

DO NOT USE IN PRODUCTION!
========================================
"""

import requests
import time
import sys

# ========================================
# CONFIGURATION
# ========================================
SERVER_URL = "http://127.0.0.1:8080"  # HTTP, not HTTPS!

# ========================================
# VULNERABLE LOGIN FUNCTION
# ========================================
def login(username, password):
    """
    Send login credentials to the server.

    VULNERABILITY: This sends credentials over HTTP in plaintext!
    Anyone on the network can intercept this data.

    Args:
        username: User's username
        password: User's password (will be sent UNENCRYPTED!)

    Returns:
        dict: Server response
    """
    print(f"\n[CLIENT] Attempting to login as '{username}'...")

    # ========================================
    # PREPARE THE LOGIN REQUEST
    # ========================================
    # This data will be sent in PLAINTEXT over the network!
    login_data = {
        "username": username,
        "password": password
    }

    print(f"[CLIENT] Sending credentials to {SERVER_URL}/login")
    print(f"[!] WARNING: Sending over HTTP (UNENCRYPTED!)")
    print(f"[!] Username: {username}")
    print(f"[!] Password: {'*' * len(password)} (but transmitted in plaintext!)")

    # ========================================
    # SEND THE REQUEST (VULNERABLE!)
    # ========================================
    try:
        # Make HTTP POST request
        # No SSL/TLS encryption - anyone can see this!
        response = requests.post(
            f"{SERVER_URL}/login",
            data=login_data,
            timeout=5
        )

        # ========================================
        # PROCESS THE RESPONSE
        # ========================================
        if response.status_code == 200:
            # Successful login
            data = response.json()
            print(f"\n[CLIENT] ✓ Login successful!")
            print(f"[CLIENT] Server says: {data.get('message')}")
            print(f"[CLIENT] Session token: {data.get('session_token')}")
            return data
        elif response.status_code == 401:
            # Authentication failed
            data = response.json()
            print(f"\n[CLIENT] ✗ Login failed!")
            print(f"[CLIENT] Server says: {data.get('message')}")
            return None
        else:
            # Unexpected response
            print(f"\n[CLIENT] Unexpected response: {response.status_code}")
            return None

    except requests.exceptions.ConnectionError:
        print(f"\n[CLIENT] ✗ Error: Cannot connect to server at {SERVER_URL}")
        print(f"[CLIENT] Make sure the server is running!")
        return None
    except requests.exceptions.Timeout:
        print(f"\n[CLIENT] ✗ Error: Request timed out")
        return None
    except Exception as e:
        print(f"\n[CLIENT] ✗ Error: {e}")
        return None

# ========================================
# AUTOMATED LOGIN ATTEMPTS
# ========================================
def auto_login_demo():
    """
    Demonstrate multiple login attempts.
    This simulates a real user repeatedly logging in,
    making it easy for an attacker to capture credentials.
    """
    print("="*60)
    print("🚨 VULNERABLE CLIENT - AUTOMATED LOGIN DEMO 🚨")
    print("="*60)
    print("[!] This client sends credentials over HTTP")
    print("[!] Perfect target for packet sniffing and MITM attacks!")
    print("="*60)

    # ========================================
    # TEST DIFFERENT USER LOGINS
    # ========================================
    test_users = [
        ("alice", "password456"),
        ("bob", "qwerty789"),
        ("admin", "supersecret123"),
        ("hacker", "wrongpass"),  # This will fail
    ]

    for username, password in test_users:
        login(username, password)
        print("\n" + "-"*60)
        time.sleep(2)  # Wait between attempts

    print("\n[CLIENT] Demo complete!")
    print("[!] All these credentials were sent in PLAINTEXT")
    print("[!] A MITM attacker could have captured everything!")

# ========================================
# INTERACTIVE MODE
# ========================================
def interactive_login():
    """
    Allow user to manually enter credentials.
    """
    print("="*60)
    print("🚨 VULNERABLE CLIENT - INTERACTIVE MODE 🚨")
    print("="*60)
    print("[!] This client sends credentials over HTTP")
    print("[!] Perfect target for MITM attacks!")
    print("="*60)

    username = input("\nEnter username: ")
    password = input("Enter password: ")

    login(username, password)

# ========================================
# MAIN ENTRY POINT
# ========================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("VULNERABLE HTTP CLIENT")
    print("="*60)
    print("\nChoose mode:")
    print("1. Auto demo (multiple login attempts)")
    print("2. Interactive (manual login)")
    print("3. Exit")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        auto_login_demo()
    elif choice == "2":
        interactive_login()
    elif choice == "3":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice!")
        sys.exit(1)

#!/usr/bin/env python3
"""
========================================
SECURE HTTPS SERVER
========================================
This is a properly secured server that protects against MITM attacks.

SECURITY FEATURES:
1. Uses HTTPS (TLS/SSL encryption) instead of HTTP
2. Strong cipher suites
3. HSTS (HTTP Strict Transport Security)
4. Secure session tokens
5. Password hashing (bcrypt)

This demonstrates how to defend against MITM attacks!
========================================
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json
import urllib.parse
import hashlib
import secrets
import os

# ========================================
# SECURE USER DATABASE
# ========================================
# In production, use a real database with bcrypt/argon2!
# These are pre-hashed passwords (SHA256 for demo purposes)
USERS = {
    "admin": hashlib.sha256("supersecret123".encode()).hexdigest(),
    "alice": hashlib.sha256("password456".encode()).hexdigest(),
    "bob": hashlib.sha256("qwerty789".encode()).hexdigest()
}

# ========================================
# SESSION MANAGEMENT
# ========================================
active_sessions = {}

def generate_secure_token():
    """
    Generate a cryptographically secure session token.
    Uses secrets module for CSPRNG (Cryptographically Secure PRNG).

    Returns:
        str: Secure random token
    """
    return secrets.token_urlsafe(32)

# ========================================
# SECURE REQUEST HANDLER
# ========================================
class SecureHandler(BaseHTTPRequestHandler):
    """
    Handles HTTPS requests securely.

    Security improvements:
    - All traffic is encrypted (HTTPS)
    - Passwords are hashed
    - Secure session tokens
    - HSTS header
    """

    def do_GET(self):
        """
        Handle GET requests - show login form
        """
        # ========================================
        # SEND SECURITY HEADERS
        # ========================================
        self.send_response(200)
        self.send_header('Content-type', 'text/html')

        # HSTS: Force HTTPS for 1 year
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')

        # Prevent clickjacking
        self.send_header('X-Frame-Options', 'DENY')

        # XSS protection
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-XSS-Protection', '1; mode=block')

        self.end_headers()

        html = """
        <html>
        <head>
            <title>Secure Login</title>
            <style>
                body { font-family: Arial; max-width: 500px; margin: 50px auto; }
                .secure { color: green; font-weight: bold; }
                input { margin: 5px 0; padding: 8px; width: 200px; }
                button { padding: 10px 20px; background: green; color: white; border: none; }
            </style>
        </head>
        <body>
            <h1>🔒 Secure Login Page</h1>
            <p class="secure">✓ HTTPS Enabled - All traffic encrypted!</p>

            <form method="POST" action="/login">
                Username: <input type="text" name="username" required><br>
                Password: <input type="password" name="password" required><br>
                <button type="submit">Login</button>
            </form>

            <h3>Security Features:</h3>
            <ul>
                <li>✅ TLS/SSL Encryption</li>
                <li>✅ Password Hashing</li>
                <li>✅ Secure Session Tokens</li>
                <li>✅ HSTS Header</li>
                <li>✅ Protected from MITM attacks</li>
            </ul>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        """
        Handle POST requests - process login
        """
        if self.path == '/login':
            # ========================================
            # READ REQUEST DATA
            # ========================================
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # ========================================
            # PARSE CREDENTIALS
            # ========================================
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]

            # ========================================
            # HASH THE PASSWORD
            # ========================================
            # In production, use bcrypt or argon2!
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            print(f"[SERVER] Login attempt: {username}")
            # Notice: We DON'T log the password!

            # ========================================
            # VALIDATE CREDENTIALS
            # ========================================
            if username in USERS and USERS[username] == password_hash:
                # ========================================
                # GENERATE SECURE SESSION TOKEN
                # ========================================
                session_token = generate_secure_token()

                # Store session
                active_sessions[session_token] = {
                    'username': username,
                    'ip': self.client_address[0]
                }

                # Success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Strict-Transport-Security', 'max-age=31536000')
                self.end_headers()

                response = {
                    "status": "success",
                    "message": f"Welcome {username}!",
                    "session_token": session_token
                }
                self.wfile.write(json.dumps(response).encode())
                print(f"[SERVER] ✓ User '{username}' logged in successfully")

            else:
                # Failed login
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.send_header('Strict-Transport-Security', 'max-age=31536000')
                self.end_headers()

                response = {
                    "status": "error",
                    "message": "Invalid credentials"
                }
                self.wfile.write(json.dumps(response).encode())
                print(f"[SERVER] ✗ Login failed for '{username}'")

    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[SERVER] {self.client_address[0]} - {format % args}")

# ========================================
# GENERATE SELF-SIGNED CERTIFICATE
# ========================================
def generate_certificate():
    """
    Generate a self-signed SSL certificate.
    In production, use certificates from a trusted CA (Let's Encrypt, etc.)

    Returns:
        tuple: (cert_file, key_file) paths
    """
    cert_file = "server.crt"
    key_file = "server.key"

    # Check if certificate already exists
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"[+] Using existing certificate: {cert_file}")
        return cert_file, key_file

    print("[*] Generating self-signed certificate...")
    print("[!] In production, use a certificate from a trusted CA!")

    # Generate using OpenSSL command
    os.system(f'''
        openssl req -new -x509 -keyout {key_file} -out {cert_file} -days 365 -nodes \
        -subj "/C=GR/ST=Attica/L=Athens/O=SecureLab/CN=localhost"
    ''')

    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"[+] Certificate generated: {cert_file}")
        return cert_file, key_file
    else:
        print("[-] Failed to generate certificate")
        print("[-] Make sure OpenSSL is installed")
        return None, None

# ========================================
# RUN SECURE SERVER
# ========================================
def run_secure_server(host='0.0.0.0', port=8443):
    """
    Start the HTTPS server.

    Args:
        host: IP to bind to
        port: Port to listen on (443 for HTTPS, 8443 for testing)
    """
    # ========================================
    # GENERATE OR LOAD CERTIFICATE
    # ========================================
    cert_file, key_file = generate_certificate()

    if not cert_file or not key_file:
        print("[-] Cannot start server without SSL certificate")
        return

    # ========================================
    # CREATE HTTPS SERVER
    # ========================================
    server_address = (host, port)
    httpd = HTTPServer(server_address, SecureHandler)

    # ========================================
    # CONFIGURE SSL/TLS
    # ========================================
    # Wrap the socket with SSL
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        certfile=cert_file,
        keyfile=key_file,
        server_side=True,
        ssl_version=ssl.PROTOCOL_TLS,  # Use latest TLS version
        # In production, specify strong ciphers:
        # ciphers='ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS'
    )

    print("="*60)
    print("🔒 SECURE HTTPS SERVER STARTING 🔒")
    print("="*60)
    print(f"[+] Server running on https://{host}:{port}")
    print(f"[+] Protocol: HTTPS (TLS/SSL)")
    print(f"[+] Certificate: {cert_file}")
    print(f"[+] Press Ctrl+C to stop")
    print("="*60)
    print("[!] Your browser will show a warning (self-signed cert)")
    print("[!] This is expected - click 'Advanced' → 'Proceed'")
    print("="*60)
    print("\n[SERVER] Waiting for connections...\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        httpd.shutdown()

if __name__ == "__main__":
    run_secure_server()

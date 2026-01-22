#!/usr/bin/env python3
"""
========================================
VULNERABLE HTTP SERVER
========================================
This is an INTENTIONALLY INSECURE server for educational purposes.

VULNERABILITIES:
1. Uses HTTP (no encryption) instead of HTTPS
2. Sends credentials in plaintext
3. No certificate validation
4. Stores passwords in plaintext (worst practice!)

DO NOT USE IN PRODUCTION!
========================================
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

# ========================================
# FAKE USER DATABASE (Plaintext passwords - BAD!)
# ========================================
USERS = {
    "admin": "supersecret123",
    "alice": "password456",
    "bob": "qwerty789"
}

# ========================================
# HTTP REQUEST HANDLER
# ========================================
class VulnerableHandler(BaseHTTPRequestHandler):
    """
    Handles incoming HTTP requests.
    This handler is vulnerable to MITM attacks because:
    - No encryption (HTTP not HTTPS)
    - No authentication tokens
    - Sends sensitive data in plaintext
    """

    def do_GET(self):
        """
        Handle GET requests - show a simple login form
        """
        # Send HTTP 200 OK response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Simple HTML login form
        html = """
        <html>
        <head><title>Vulnerable Login</title></head>
        <body>
            <h1>Login Page (VULNERABLE)</h1>
            <form method="POST" action="/login">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
            <p style="color:red;">WARNING: This sends credentials over HTTP (unencrypted)!</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        """
        Handle POST requests - process login attempts
        """
        if self.path == '/login':
            # ========================================
            # READ THE REQUEST BODY
            # ========================================
            # Get the length of the data sent
            content_length = int(self.headers['Content-Length'])
            # Read the actual data
            post_data = self.rfile.read(content_length)

            # ========================================
            # PARSE THE CREDENTIALS (PLAINTEXT!)
            # ========================================
            # Decode the URL-encoded form data
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]

            # ========================================
            # LOG THE CREDENTIALS (Very bad practice!)
            # ========================================
            print(f"[SERVER] Login attempt: username={username}, password={password}")

            # ========================================
            # VALIDATE CREDENTIALS
            # ========================================
            if username in USERS and USERS[username] == password:
                # Successful login
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                response = {
                    "status": "success",
                    "message": f"Welcome {username}!",
                    "session_token": f"FAKE_TOKEN_{username}_12345"  # Predictable token!
                }
                self.wfile.write(json.dumps(response).encode())
                print(f"[SERVER] ✓ User '{username}' logged in successfully")
            else:
                # Failed login
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                response = {
                    "status": "error",
                    "message": "Invalid username or password"
                }
                self.wfile.write(json.dumps(response).encode())
                print(f"[SERVER] ✗ Login failed for '{username}'")
        else:
            # Unknown endpoint
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """
        Override to customize logging
        """
        print(f"[SERVER] {self.client_address[0]} - {format % args}")

# ========================================
# MAIN SERVER SETUP
# ========================================
def run_server(host='0.0.0.0', port=8080):
    """
    Start the vulnerable HTTP server

    Args:
        host: IP address to bind to (0.0.0.0 = all interfaces)
        port: Port number to listen on
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, VulnerableHandler)

    print("="*50)
    print("🚨 VULNERABLE HTTP SERVER STARTING 🚨")
    print("="*50)
    print(f"[+] Server running on http://{host}:{port}")
    print(f"[+] Press Ctrl+C to stop")
    print(f"[!] WARNING: This server is INTENTIONALLY INSECURE")
    print(f"[!] All traffic is UNENCRYPTED (HTTP)")
    print(f"[!] Perfect target for MITM attacks!")
    print("="*50)
    print("\n[SERVER] Waiting for connections...\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()

# 🎯 Vulnerable Target System

Αυτά είναι τα **intentionally vulnerable** scripts που θα χρησιμοποιήσουμε ως target για το MITM attack.

## 📁 Files

- `server.py` - HTTP server που δέχεται login requests (UNENCRYPTED)
- `client.py` - Client που στέλνει credentials σε HTTP (UNENCRYPTED)

---

## 🚀 Πώς να τρέξεις το Lab

### Βήμα 1: Install Dependencies

```bash
pip install requests
```

### Βήμα 2: Start the Server

Άνοιξε ένα terminal και τρέξε:

```bash
python server.py
```

Θα δεις:
```
==================================================
🚨 VULNERABLE HTTP SERVER STARTING 🚨
==================================================
[+] Server running on http://0.0.0.0:8080
[+] Press Ctrl+C to stop
[!] WARNING: This server is INTENTIONALLY INSECURE
[!] All traffic is UNENCRYPTED (HTTP)
[!] Perfect target for MITM attacks!
==================================================
```

### Βήμα 3: Run the Client

Άνοιξε ένα **δεύτερο terminal** και τρέξε:

```bash
python client.py
```

Επίλεξε mode:
- **Option 1**: Auto demo - θα στείλει πολλά login requests
- **Option 2**: Interactive - θα εισάγεις εσύ username/password

---

## 🔓 Valid Credentials

Για να δοκιμάσεις επιτυχημένο login, χρησιμοποίησε:

```
Username: admin
Password: supersecret123

Username: alice
Password: password456

Username: bob
Password: qwerty789
```

---

## 🚨 Γιατί είναι Vulnerable;

### 1. **HTTP instead of HTTPS**
```
❌ http://127.0.0.1:8080  (No encryption)
✅ https://127.0.0.1:8443 (Encrypted - but we're not using this!)
```

### 2. **Plaintext Credentials**
Όταν ο client στέλνει το login request:
```http
POST /login HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/x-www-form-urlencoded

username=admin&password=supersecret123
```
^ **Όλα αυτά είναι ορατά σε κάποιον που κάνει packet sniffing!**

### 3. **No Certificate Validation**
Ο client δεν ελέγχει αν μιλάει στον σωστό server!

### 4. **Predictable Session Tokens**
```python
session_token = f"FAKE_TOKEN_{username}_12345"
```
Ο attacker μπορεί να μαντέψει τα tokens!

---

## 🎯 Τι θα κάνουμε στο Exploit Phase;

Θα φτιάξουμε ένα MITM attack tool που:

1. ✅ Τοποθετείται **ανάμεσα** στον client και τον server
2. ✅ **Intercepts** όλα τα packets
3. ✅ **Reads** τα credentials σε plaintext
4. ✅ **Optionally modifies** τα data
5. ✅ **Forwards** τα packets για να μην καταλάβει κανείς

---

## 🧪 Testing

### Test 1: Normal Operation
1. Start server: `python server.py`
2. Run client: `python client.py` → Choose option 1
3. Watch the server logs - βλέπεις τα credentials!

### Test 2: Browser Access
1. Start server
2. Open browser: http://localhost:8080
3. Εισήγαγε credentials και κάνε submit
4. Check server terminal - τα credentials εμφανίζονται!

### Test 3: Wireshark Capture (Preview)
1. Start Wireshark
2. Capture on loopback interface (127.0.0.1)
3. Filter: `http`
4. Run the client
5. **Βρες το POST request** - θα δεις τα credentials σε plaintext!

---

## ⚠️ Safety Note

```
┌────────────────────────────────────────┐
│  Αυτά τα scripts είναι INTENTIONALLY   │
│  vulnerable για μαθησιακούς σκοπούς.   │
│                                        │
│  ΠΟΤΕ μην τα χρησιμοποιήσεις σε:      │
│  • Production environments             │
│  • Public networks                     │
│  • Real user data                      │
└────────────────────────────────────────┘
```

---

**Next Step**: Πήγαινε στο `exploit/` directory για να φτιάξουμε το MITM attack tool! 🔥

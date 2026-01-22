# 🟢 Challenge 1: HTTP Credential Sniffing (EASY)

## 📋 Objective

Capture username and password από ένα HTTP login request χρησιμοποιώντας packet sniffing.

**Δυσκολία**: 🟢 Beginner
**Χρόνος**: ~15 λεπτά
**Skills**: Packet sniffing, HTTP analysis

---

## 🎯 Στόχος

Θα τρέξεις:
1. Έναν vulnerable HTTP server
2. Έναν client που θα κάνει login
3. Ένα packet sniffer που θα **capture τα credentials**

**Mission**: Capture τουλάχιστον 3 διαφορετικά credentials!

---

## 📚 Background Info

Όταν ένας client στέλνει credentials μέσω HTTP:
```
POST /login HTTP/1.1
Host: localhost:8080
Content-Type: application/x-www-form-urlencoded

username=alice&password=password456
```

Αυτά τα δεδομένα **δεν είναι κρυπτογραφημένα**!
Οποιοσδήποτε στο ίδιο network μπορεί να τα διαβάσει.

---

## 🚀 Step-by-Step Walkthrough

### Step 1: Prepare Your Terminal Windows

Άνοιξε **3 terminals** (ή tabs):
- Terminal 1: Server
- Terminal 2: Packet Sniffer
- Terminal 3: Client

### Step 2: Start the Vulnerable Server

**Terminal 1**:
```bash
cd ../../vulnerable/
python server.py
```

**Expected output**:
```
🚨 VULNERABLE HTTP SERVER STARTING 🚨
[+] Server running on http://0.0.0.0:8080
[SERVER] Waiting for connections...
```

✅ **Checkpoint**: Βλέπεις το μήνυμα "Server running"?

### Step 3: Start the Packet Sniffer

**Terminal 2**:
```bash
cd ../../exploit/
sudo python3 packet_sniffer.py
```

Θα σε ρωτήσει: "Do you understand and want to continue?"
Type: **yes**

**Expected output**:
```
🎣 HTTP PACKET SNIFFER - CREDENTIAL HARVESTER
==========================================
[*] Monitoring ports: [80, 8080, 8000, 3000]
[*] Listening for HTTP traffic...
```

✅ **Checkpoint**: Βλέπεις "Listening for HTTP traffic"?

### Step 4: Run the Client

**Terminal 3**:
```bash
cd ../../vulnerable/
python client.py
```

Επίλεξε: **1** (Auto demo)

**Expected output** (Terminal 3 - Client):
```
[CLIENT] Attempting to login as 'alice'...
[CLIENT] Sending credentials to http://127.0.0.1:8080/login
[CLIENT] ✓ Login successful!
```

### Step 5: Check the Sniffer Output

**Go to Terminal 2** (Packet Sniffer)

**You should see**:
```
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🎯 CREDENTIALS CAPTURED!
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
Username: alice
Password: password456
Source:   127.0.0.1
...
```

🎉 **Congratulations!** Μόλις έκανες capture credentials από HTTP traffic!

### Step 6: Stop and Review

1. Press **Ctrl+C** σε όλα τα terminals
2. Check το file `captured_credentials.txt` στο exploit folder:
   ```bash
   cat ../../exploit/captured_credentials.txt
   ```

---

## ✅ Success Criteria

Για να ολοκληρώσεις το challenge, πρέπει:

- [ ] Να έχεις captured **τουλάχιστον 3** credentials
- [ ] Να βλέπεις τα credentials στο sniffer output
- [ ] Να υπάρχει το file `captured_credentials.txt` με τα αποτελέσματα

---

## 💡 Hints

<details>
<summary>Hint 1: Δεν βλέπω credentials στο sniffer</summary>

**Possible issues**:
1. Ο sniffer τρέχει με sudo? (Χρειάζεται root privileges)
2. Το INTERFACE στο `packet_sniffer.py` είναι σωστό?
   - Windows: Μπορεί να χρειαστεί "loopback" ή διαφορετικό interface
   - Linux/Mac: Συνήθως "lo" ή "lo0" για localhost traffic

**Solution**:
Edit `packet_sniffer.py` line 24:
```python
INTERFACE = "lo"  # Try "lo", "lo0", or "loopback"
```
</details>

<details>
<summary>Hint 2: "Permission denied" error</summary>

Packet sniffing χρειάζεται **root/admin privileges**.

**Linux/Mac**:
```bash
sudo python3 packet_sniffer.py
```

**Windows**:
Run terminal as Administrator
</details>

<details>
<summary>Hint 3: Client can't connect to server</summary>

**Check**:
1. Ο server τρέχει; (Terminal 1)
2. Το port 8080 είναι free;

**Test**:
```bash
curl http://localhost:8080
# Should show HTML login form
```
</details>

---

## 🤔 Questions to Think About

1. **Γιατί μπορούμε να δούμε τα credentials;**
   <details>
   <summary>Answer</summary>
   Επειδή το HTTP δεν έχει encryption. Όλα τα data στέλνονται σε plaintext.
   </details>

2. **Σε real-world scenario, πότε θα μπορούσε να γίνει αυτό;**
   <details>
   <summary>Answer</summary>
   - Σε public Wi-Fi (Starbucks, airport, etc.)
   - Σε compromised routers
   - Σε corporate networks χωρίς encryption
   </details>

3. **Πώς θα το αποτρέψουμε;**
   <details>
   <summary>Answer</summary>
   - Χρήση HTTPS αντί για HTTP
   - VPN για encryption
   - Network segmentation
   </details>

---

## 🎓 What You Learned

✅ Πώς να κάνεις packet sniffing με Scapy
✅ Πώς να εξάγεις credentials από HTTP traffic
✅ Γιατί το HTTP είναι ανασφαλές
✅ Πώς να χρησιμοποιείς το sniffer tool

---

## 🚀 Next Steps

Ready for more? Try:

1. **🟡 Medium Challenge**: ARP Spoofing σε real network
2. **Experiment**: Δοκίμασε να sniff traffic από browser
   - Άνοιξε http://localhost:8080 στον browser
   - Login με username/password
   - Έπιασε το sniffer τα credentials;

3. **Defense**: Δοκίμασε το secure_server.py
   - Μπορείς να sniff HTTPS credentials;
   - Τι διαφορά βλέπεις;

---

**Excellent work! 🎉 You've completed the Easy challenge!**

Next: `../02-medium/` για περισσότερο challenge!

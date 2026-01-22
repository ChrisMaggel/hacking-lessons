# 🛡️ Defense Mechanisms - Protection Against MITM

Εδώ θα μάθεις πώς να **προστατευτείς** από Man-in-the-Middle attacks!

## 📁 Files

1. **`secure_server.py`** - HTTPS server με encryption και security headers
2. **`arp_detector.py`** - Tool για detection ARP spoofing attacks

---

## 🔒 Defense Strategy

### Layer 1: Encryption (HTTPS)
**Problem**: HTTP sends data in plaintext
**Solution**: Use HTTPS (TLS/SSL) to encrypt all traffic

### Layer 2: Authentication (Certificates)
**Problem**: Attacker can fake servers
**Solution**: Verify SSL certificates

### Layer 3: Detection (Monitoring)
**Problem**: Silent attacks are hard to catch
**Solution**: Monitor for suspicious ARP activity

---

## 🚀 Running the Secure Server

### Step 1: Start the HTTPS Server

```bash
python secure_server.py
```

**First run** - generates self-signed certificate:
```
[*] Generating self-signed certificate...
[+] Certificate generated: server.crt
🔒 SECURE HTTPS SERVER STARTING 🔒
[+] Server running on https://0.0.0.0:8443
[+] Protocol: HTTPS (TLS/SSL)
```

### Step 2: Access from Browser

```
https://localhost:8443
```

**⚠️ You'll see a warning**: "Your connection is not private"

**Why?** Self-signed certificates aren't trusted by default.

**What to do:**
1. Click "Advanced"
2. Click "Proceed to localhost (unsafe)"

**In production**, use certificates from:
- Let's Encrypt (free!)
- DigiCert
- Comodo
- etc.

---

## 🔐 What Makes This Server Secure?

### 1. HTTPS Encryption
```python
# All traffic is encrypted with TLS/SSL
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    certfile=cert_file,
    keyfile=key_file,
    ssl_version=ssl.PROTOCOL_TLS
)
```

**Result**: Even if attacker intercepts packets, they see encrypted gibberish:
```
16 03 03 00 4a 01 00 00 46 03 03 5e 8f 2a 1c...
```
Instead of:
```
username=admin&password=supersecret123
```

### 2. HSTS Header
```python
'Strict-Transport-Security': 'max-age=31536000'
```

**What it does**: Forces browser to ALWAYS use HTTPS for this domain
**Protection**: Prevents SSL stripping attacks

### 3. Password Hashing
```python
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

**Result**: Database stores hashes, not plaintext passwords
**Note**: In production, use bcrypt or argon2!

### 4. Secure Session Tokens
```python
session_token = secrets.token_urlsafe(32)
```

**Before** (vulnerable):
```
FAKE_TOKEN_admin_12345  ← Predictable!
```

**After** (secure):
```
Xj8kP2mNq7vR4wZ9tY3sL6hF1aD5gK0c...  ← Random!
```

---

## 🕵️ ARP Spoofing Detector

### What It Detects:

1. **MAC Address Changes**
   ```
   192.168.1.10 was AA:BB:CC:DD:EE:FF
   Now it's      11:22:33:44:55:66  ← ATTACK!
   ```

2. **Gratuitous ARP**
   ```
   "I am 192.168.1.1 at MAC XX:XX:XX:XX"
   (But you're not the real gateway!)
   ```

3. **ARP Flooding**
   ```
   Normal:  2-3 ARP packets/second
   Attack:  100+ ARP packets/second  ← FLOOD!
   ```

### How to Use:

```bash
sudo python3 arp_detector.py
```

**Output** (normal operation):
```
🕵️  ARP SPOOFING DETECTOR
==========================================
[14:32:10] New device: 192.168.1.1 → AA:BB:CC:DD:EE:FF
[14:32:15] New device: 192.168.1.100 → 11:22:33:44:55:66
```

**Output** (attack detected):
```
============================================================
🚨 ARP SPOOFING DETECTED! 🚨
============================================================
Time:     14:35:22
IP:       192.168.1.1
Old MAC:  AA:BB:CC:DD:EE:FF
New MAC:  99:88:77:66:55:44
Type:     ARP Reply
============================================================
```

All attacks are logged to `arp_attacks.log`!

---

## 🧪 Testing the Defense

### Test 1: HTTPS vs HTTP Sniffing

**Setup**:
1. Terminal 1: `sudo python3 ../exploit/packet_sniffer.py`
2. Terminal 2: `python secure_server.py`
3. Browser: Visit `https://localhost:8443` and login

**Result**: The sniffer **cannot read** your credentials! 🎉

**Why?** HTTPS encrypts the data. The sniffer only sees:
```
[+] HTTP Packet Captured!
    [Encrypted TLS data - cannot read]
```

### Test 2: ARP Spoofing Detection

**Setup**:
1. Terminal 1: `sudo python3 arp_detector.py`
2. Terminal 2: `sudo python3 ../exploit/arp_spoof.py`

**Result**: The detector **immediately alerts** you! 🚨

```
🚨 ARP SPOOFING DETECTED! 🚨
IP:       192.168.1.100
Old MAC:  [real MAC]
New MAC:  [attacker's MAC]
```

---

## 📊 Security Comparison

| Feature | Vulnerable Server | Secure Server |
|---------|------------------|---------------|
| Protocol | HTTP | HTTPS |
| Password storage | Plaintext | Hashed (SHA256/bcrypt) |
| Session tokens | Predictable | Cryptographically random |
| HSTS | ❌ No | ✅ Yes |
| Certificate | ❌ No | ✅ Yes (self-signed) |
| **MITM vulnerable?** | ✅ YES | ❌ NO |

---

## 🔧 Additional Security Measures

### For Networks:

#### 1. Static ARP Entries
```bash
# Manually set gateway's ARP entry (can't be spoofed)
sudo arp -s 192.168.1.1 AA:BB:CC:DD:EE:FF
```

#### 2. Port Security (Switch Level)
```
# Cisco switch example
switchport port-security
switchport port-security mac-address [MAC]
switchport port-security violation shutdown
```

#### 3. Dynamic ARP Inspection (DAI)
```
# Validates ARP packets against DHCP snooping database
ip arp inspection vlan 10
```

---

### For Users:

#### 1. Use VPN
```
All traffic encrypted end-to-end
Even on untrusted Wi-Fi!
```

#### 2. Browser Extensions
- **HTTPS Everywhere** - Forces HTTPS
- **Certificate Patrol** - Alerts on cert changes

#### 3. Check SSL Certificates
```
Click the padlock icon → Certificate info
Verify:
- Issued to: example.com
- Issued by: [Trusted CA]
- Valid dates
```

---

## 🔍 How to Verify HTTPS is Working

### Method 1: Browser
Look for **🔒 padlock icon** in address bar

### Method 2: Developer Tools
1. Open Dev Tools (F12)
2. Go to Network tab
3. Check Protocol column: Should say "h2" or "https"

### Method 3: Command Line
```bash
curl -I https://localhost:8443
```

Output should include:
```
HTTP/2 200
strict-transport-security: max-age=31536000
```

### Method 4: Wireshark
1. Capture traffic
2. Filter: `tcp.port == 8443`
3. See "TLSv1.2" or "TLSv1.3" instead of "HTTP"

---

## ⚡ Real-World Defense Tools

### Network Monitoring:
- **Wireshark** - Packet analysis
- **arpwatch** - ARP monitoring daemon
- **Snort** - Intrusion detection
- **Suricata** - Network security monitoring

### Certificate Management:
- **Let's Encrypt** - Free SSL certificates
- **Certbot** - Automated cert installation
- **cert-manager** - Kubernetes cert automation

### VPN Solutions:
- **OpenVPN** - Open source VPN
- **WireGuard** - Modern, fast VPN
- **IPSec** - Industry standard

---

## 📚 Best Practices

### For Developers:

```
✅ DO:
- Always use HTTPS in production
- Use HSTS headers
- Implement certificate pinning (mobile apps)
- Hash passwords with bcrypt/argon2
- Use secure session management
- Keep TLS libraries updated

❌ DON'T:
- Use HTTP for sensitive data
- Ignore certificate warnings
- Store plaintext passwords
- Use predictable tokens
- Trust client-side validation only
```

### For Users:

```
✅ DO:
- Use VPN on public Wi-Fi
- Check for HTTPS (padlock icon)
- Keep browsers updated
- Use password managers
- Enable 2FA everywhere

❌ DON'T:
- Ignore certificate warnings
- Login on HTTP sites
- Use same password everywhere
- Trust public Wi-Fi for banking
- Click "Proceed anyway" without thinking
```

---

## 🎯 Challenge Yourself!

Try these exercises:

1. **Run ARP detector while performing ARP spoofing**
   - Does it catch the attack?
   - How many packets before detection?

2. **Try to sniff HTTPS traffic**
   - Can you see the credentials?
   - What do you see instead?

3. **Modify the secure server**
   - Implement certificate pinning
   - Add rate limiting for logins
   - Implement 2FA

---

## 📖 Further Reading

- **OWASP HTTPS Guide**: https://owasp.org/www-community/Transport_Layer_Security_Cheat_Sheet
- **Mozilla SSL Config Generator**: https://ssl-config.mozilla.org/
- **Let's Encrypt**: https://letsencrypt.org/
- **ARP Spoofing Defense**: https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/12-2/25ew/configuration/guide/conf/dynarp.html

---

**Next**: Time for challenges! 🎮 Go to `challenges/` directory!

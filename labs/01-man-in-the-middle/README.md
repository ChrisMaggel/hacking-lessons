# 🎭 Man-in-the-Middle (MITM) Attack

## 📚 Τι είναι το MITM; (ELI5 - Explain Like I'm 5)

Φανταστείτε ότι στέλνετε ένα μυστικό γράμμα στον φίλο σας μέσω ενός αγγελιοφόρου.
Αλλά ο "αγγελιοφόρος" είναι στην πραγματικότητα ένας κακόβουλος άνθρωπος που:
1. 📬 **Παραλαμβάνει** το γράμμα σας
2. 👀 **Το διαβάζει** (ή το αλλάζει!)
3. 📮 **Το στέλνει** στον φίλο σας σαν να μην έγινε τίποτα

Εσείς και ο φίλος σας νομίζετε ότι επικοινωνείτε απευθείας, αλλά στην πραγματικότητα **υπάρχει κάποιος στη μέση** που βλέπει (ή τροποποιεί) τα πάντα!

---

## 🔬 Τεχνική Εξήγηση

Το **Man-in-the-Middle (MITM)** είναι μια επίθεση όπου ο εισβολέας παρεμβάλλεται **ανάμεσα** σε δύο επικοινωνούντα μέρη (π.χ. client-server, user-website) χωρίς η επικοινωνία να διακοπεί.

### Πώς λειτουργεί:

```
ΚΑΝΟΝΙΚΗ ΕΠΙΚΟΙΝΩΝΙΑ:
[Client] ←→ [Server]

MITM ATTACK:
[Client] ←→ [Attacker] ←→ [Server]
           (Μιμείται     (Μιμείται
            τον Server)   τον Client)
```

### Τύποι MITM Attacks:

1. **ARP Spoofing**: Δηλητηρίαση του ARP cache για redirect traffic
2. **DNS Spoofing**: Fake DNS responses για redirect σε κακόβουλους servers
3. **HTTPS Spoofing**: SSL stripping ή fake certificates
4. **Wi-Fi Eavesdropping**: Rogue access points (Evil Twin)
5. **Session Hijacking**: Κλοπή session tokens

---

## 🌍 Πραγματικά Παραδείγματα Επιθέσεων

### 1. **Starbucks Wi-Fi Hack (2014)**
- Hacker έστησε **fake Wi-Fi hotspot** με το όνομα "Starbucks WiFi"
- Χρήστες συνδέθηκαν νομίζοντας ότι είναι το επίσημο
- Ο hacker έβλεπε **όλη την κίνηση**: passwords, emails, banking

### 2. **Lenovo Superfish (2015)**
- Η Lenovo προεγκατέστησε adware που **έκανε install fake certificate**
- Το malware μπορούσε να κάνει MITM σε **HTTPS connections**
- Επηρέασε εκατομμύρια laptops

### 3. **Public Wi-Fi Banking Theft (2017)**
- Επιτιθέμενοι σε καφετέριες έστηναν **rogue access points**
- Έκλεβαν **banking credentials** από users που συνδέονταν
- Απώλειες εκατοντάδων χιλιάδων δολαρίων

### 4. **Email Interception - Business Email Compromise (2019)**
- Hackers έκαναν MITM σε **email επικοινωνία** εταιρειών
- Τροποποίησαν **αριθμούς λογαριασμών** σε τιμολόγια
- Εταιρείες έστειλαν **χρήματα σε λάθος λογαριασμούς**

---

## ⚙️ Γιατί Δουλεύει; (Underlying Vulnerability)

### 1. **Lack of Encryption**
- HTTP traffic είναι **plaintext** → εύκολο sniffing
- Unencrypted Wi-Fi → πλήρης ορατότητα

### 2. **Trust in Network**
- Τα συστήματα **εμπιστεύονται** το local network
- Δεν επαληθεύουν την **ταυτότητα** του άλλου μέρους

### 3. **ARP Protocol Weakness**
- Το ARP **δεν έχει authentication**
- Οποιοσδήποτε μπορεί να στείλει fake ARP replies
- Το OS **δέχεται gratuitous ARP** χωρίς έλεγχο

### 4. **DNS Lacks Validation**
- Το DNS **δεν επαληθεύει** την πηγή των responses
- First response wins → race condition

### 5. **Certificate Trust Issues**
- Users **παραβλέπουν** certificate warnings
- Malware μπορεί να **εγκαταστήσει trusted root CAs**

---

## 🛡️ Πώς να Προστατευτείς

### Για Users:

#### 1. **Χρησιμοποίησε HTTPS Everywhere**
```
✅ https://example.com  (Encrypted)
❌ http://example.com   (Plaintext)
```

#### 2. **VPN (Virtual Private Network)**
- Κρυπτογραφεί **όλη τη traffic** σου
- Ακόμα και σε untrusted Wi-Fi

#### 3. **Πρόσεχε τα Certificate Warnings**
```
⚠️ "Your connection is not private"
⚠️ "Invalid certificate"
→ ΜΗΝ συνεχίσεις!
```

#### 4. **Απόφυγε Public Wi-Fi για Sensitive Tasks**
- Μην κάνεις banking σε Starbucks Wi-Fi
- Μην εισάγεις passwords σε δημόσια δίκτυα

#### 5. **Ενεργοποίησε Two-Factor Authentication (2FA)**
- Ακόμα κι αν κλαπεί το password, χρειάζεται το 2FA

---

### Για Developers/Admins:

#### 1. **Enforce HTTPS με HSTS**
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

#### 2. **Certificate Pinning**
```python
# Αποδοχή ΜΟΝΟ συγκεκριμένου certificate
expected_cert = "sha256/AAAAAAAAAA..."
```

#### 3. **Mutual TLS (mTLS)**
- Και ο client ΚΑΙ ο server επαληθεύουν ταυτότητα

#### 4. **ARP Spoofing Detection**
```bash
# Static ARP entries για critical systems
arp -s 192.168.1.1 00:11:22:33:44:55
```

#### 5. **DNSSEC (DNS Security Extensions)**
- Cryptographic signatures για DNS responses

#### 6. **Network Segmentation**
- Χωρισμός δικτύων σε VLANs
- Όχι flat networks

---

## 🔍 Detection Methods

### 1. **Monitor ARP Tables**
```bash
# Έλεγξε για duplicate IP/MAC mappings
arp -a
```

### 2. **Network Traffic Analysis**
- Wireshark filters:
```
arp.duplicate-address-detected
```

### 3. **Certificate Monitoring**
```bash
# Έλεγξε το certificate fingerprint
openssl s_client -connect example.com:443 | openssl x509 -fingerprint -noout
```

### 4. **Latency Detection**
- MITM προσθέτει **extra latency**
- Monitor για αύξηση RTT (Round Trip Time)

---

## 📊 MITM Attack Chain

```
1. RECONNAISSANCE
   ↓
   [Scan network, identify targets]

2. POSITIONING
   ↓
   [ARP Spoofing / Rogue AP / DNS Poisoning]

3. INTERCEPTION
   ↓
   [Forward packets between victim & server]

4. EXPLOITATION
   ↓
   [Steal credentials / Modify data / Inject malware]

5. COVERING TRACKS
   ↓
   [Restore ARP tables / Delete logs]
```

---

## 🎯 Τι θα μάθεις σε αυτό το Lab

1. ✅ Πώς να στήσεις ένα **vulnerable client-server system**
2. ✅ Πώς να κάνεις **ARP spoofing** για MITM
3. ✅ Πώς να **intercept και modify** HTTP traffic
4. ✅ Πώς να **steal credentials** από unencrypted connections
5. ✅ Πώς να **detect** MITM attacks
6. ✅ Πώς να **αμυνθείς** με encryption & validation

---

## ⚠️ Legal & Ethical Disclaimer

```
┌─────────────────────────────────────────────────────┐
│  ⚖️  ΜΟΝΟ ΓΙΑ EDUCATIONAL PURPOSES!                │
│                                                     │
│  • Χρησιμοποίησε ΜΟΝΟ σε controlled lab environment│
│  • ΠΟΤΕ σε production systems χωρίς άδεια          │
│  • Unauthorized MITM attacks = ΠΑΡΑΝΟΜΕΣ           │
│  • Respect privacy & laws                          │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Δομή του Lab

```
01-man-in-the-middle/
├── README.md           ← (Είσαι εδώ!)
├── vulnerable/         ← Ευάλωτα client/server scripts
├── exploit/            ← MITM attack tools
├── defense/            ← Protection implementations
└── challenges/         ← Πρακτικές ασκήσεις
```

---

**Ετοιμάσου για hands-on hacking! 🚀**

Next: `vulnerable/` - Θα φτιάξουμε το target system!

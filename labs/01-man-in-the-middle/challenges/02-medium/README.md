# 🟡 Challenge 2: ARP Poisoning Attack (MEDIUM)

## 📋 Objective

Εκτέλεσε ένα **πραγματικό ARP spoofing attack** σε local network για να τοποθετηθείς ως Man-in-the-Middle ανάμεσα σε δύο συσκευές.

**Δυσκολία**: 🟡 Intermediate
**Χρόνος**: ~30 λεπτά
**Skills**: ARP protocol, network reconnaissance, MITM positioning

---

## 🎯 Mission

Πρέπει να:
1. ✅ Identify 2 targets στο network (victim + gateway)
2. ✅ Perform ARP spoofing για να γίνεις MITM
3. ✅ Capture τουλάχιστον 1 HTTP request από το victim
4. ✅ Restore το ARP table μετά την επίθεση

**Bonus**: Modify ένα HTTP request in-flight!

---

## 🔧 Setup Requirements

### Option A: Virtual Machines (Recommended)
- **VM 1**: Attacker machine (you) - με Python & Scapy
- **VM 2**: Victim machine
- **VM 3**: Server machine (running vulnerable HTTP server)
- Όλα σε **Bridged** ή **Internal Network** mode

### Option B: Physical Devices
- Τουλάχιστον 2 devices στο ίδιο Wi-Fi/LAN
- ⚠️ **ΜΟΝΟ σε δίκτυο που το ελέγχεις εσύ!**

### Option C: Docker Containers (Advanced)
- 3 containers σε custom bridge network

---

## 📚 Background Theory

### Πώς λειτουργεί το ARP Spoofing:

**Normal ARP Communication**:
```
Victim:  "Who has 192.168.1.1? Tell me at MAC AA:AA:AA:AA:AA:AA"
Gateway: "192.168.1.1 is at MAC BB:BB:BB:BB:BB:BB"

Victim's ARP Table:
192.168.1.1  →  BB:BB:BB:BB:BB:BB  ✅ (correct)
```

**After ARP Spoofing**:
```
Attacker → Victim:  "192.168.1.1 is at MAC XX:XX:XX:XX:XX:XX" (lie!)
Attacker → Gateway: "192.168.1.100 is at MAC XX:XX:XX:XX:XX:XX" (lie!)

Victim's ARP Table:
192.168.1.1  →  XX:XX:XX:XX:XX:XX  ❌ (poisoned!)

Gateway's ARP Table:
192.168.1.100  →  XX:XX:XX:XX:XX:XX  ❌ (poisoned!)

Now all traffic flows through the attacker!
```

---

## 🗺️ High-Level Steps (Figure it out!)

Σου δίνω τα **γενικά βήματα**, αλλά πρέπει να σκεφτείς **πώς** ακριβώς να τα κάνεις:

### Phase 1: Reconnaissance
1. Βρες το **IP του gateway** (router)
2. Βρες το **IP του victim**
3. Βρες τα **MAC addresses** και των δύο

### Phase 2: Setup
1. Enable **IP forwarding** στο attacker machine
2. Prepare το **ARP spoofing script**
3. Prepare το **packet sniffer**

### Phase 3: Attack
1. Start **ARP poisoning**
2. Start **packet capture**
3. Victim κάνει HTTP request → **capture it!**

### Phase 4: Cleanup
1. Stop ARP spoofing
2. **Restore** ARP tables
3. Verify victim's connection is OK

---

## 💡 Partial Hints (Use if stuck!)

<details>
<summary>Hint 1: Πώς βρίσκω το gateway IP;</summary>

**Linux/Mac**:
```bash
ip route | grep default
# OR
route -n | grep ^0.0.0.0
```

**Windows**:
```bash
ipconfig | findstr "Default Gateway"
```

**Output example**:
```
default via 192.168.1.1 dev eth0
```
→ Gateway is `192.168.1.1`
</details>

<details>
<summary>Hint 2: Πώς βρίσκω άλλες συσκευές στο network;</summary>

**Method 1**: nmap scan
```bash
nmap -sn 192.168.1.0/24
```

**Method 2**: arp-scan
```bash
sudo arp-scan --localnet
```

**Method 3**: Check router's DHCP table
- Login στο router (http://192.168.1.1)
- Δες connected devices
</details>

<details>
<summary>Hint 3: Πώς enable IP forwarding;</summary>

**Linux**:
```bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

**Mac**:
```bash
sudo sysctl -w net.inet.ip.forwarding=1
```

**Verify**:
```bash
cat /proc/sys/net/ipv4/ip_forward
# Should show: 1
```

**Γιατί χρειάζεται;**
Χωρίς IP forwarding, packets θα drop → victim θα χάσει internet!
</details>

<details>
<summary>Hint 4: Πώς τρέχω το ARP spoofing;</summary>

1. **Edit** `../../exploit/arp_spoof.py`:
   ```python
   TARGET_IP = "192.168.1.XXX"    # Victim's IP
   GATEWAY_IP = "192.168.1.1"     # Gateway IP
   INTERFACE = "eth0"             # Your interface
   ```

2. **Run**:
   ```bash
   sudo python3 ../../exploit/arp_spoof.py
   ```

3. **Verify it's working**:
   On victim machine:
   ```bash
   arp -a
   # Check if gateway's MAC = your MAC (not the real gateway's MAC)
   ```
</details>

<details>
<summary>Hint 5: Πώς verify ότι είμαι MITM;</summary>

**On Victim machine**:
```bash
# Check ARP table
arp -a | grep [GATEWAY_IP]

# Before attack:
192.168.1.1  →  aa:bb:cc:dd:ee:ff

# During attack:
192.168.1.1  →  11:22:33:44:55:66  ← YOUR MAC!
```

**On Attacker machine**:
```bash
# Monitor traffic flowing through you
sudo tcpdump -i eth0 host [VICTIM_IP]
# You should see packets!
```
</details>

---

## 🧪 Verification

### Test 1: Can victim still browse the internet?

**On victim machine**:
```bash
ping google.com
# Should work (because you're forwarding traffic)
```

✅ If YES → You're successfully MITM!
❌ If NO → Check IP forwarding

### Test 2: Are you capturing traffic?

**On attacker machine** (with packet_sniffer running):
- Victim visits `http://example.com`
- You should see the HTTP requests!

### Test 3: Can you capture credentials?

**Setup**:
1. Run vulnerable server on a 3rd machine (or your machine)
2. Victim visits that server and logins
3. You capture the credentials!

---

## 🎯 Success Criteria

Mark off each requirement:

- [ ] Successfully identified gateway and victim IPs
- [ ] Enabled IP forwarding on attacker machine
- [ ] Ran ARP spoofing script without errors
- [ ] Verified ARP poisoning (victim's ARP table shows your MAC)
- [ ] Victim can still access internet (traffic forwarded through you)
- [ ] Captured at least 1 HTTP request from victim
- [ ] Properly restored ARP tables after attack
- [ ] Victim's internet works normally after cleanup

**Bonus**:
- [ ] Captured credentials from HTTP login
- [ ] Modified an HTTP request/response (using mitm_proxy.py)

---

## ⚠️ Troubleshooting

### "Victim lost internet connection"
→ Check IP forwarding: `cat /proc/sys/net/ipv4/ip_forward` (should be 1)

### "ARP spoofing not working"
→ Verify you're on the same network segment (same subnet)
→ Check if your network interface is correct

### "Can't capture packets"
→ Make sure packet_sniffer.py is using the right interface
→ Run with sudo

### "Permission denied"
→ All these tools need root: `sudo python3 script.py`

---

## 🤔 Reflection Questions

1. **Γιατί χρειάζεται IP forwarding;**
   - Τι θα γινόταν αν δεν το είχαμε enable;

2. **Πώς θα καταλάβει ένας admin ότι γίνεται ARP spoofing;**
   - Ποια tools θα μπορούσε να χρησιμοποιήσει;

3. **Σε production network, γιατί αυτή η επίθεση είναι δύσκολη;**
   - Ποια security measures θα την εμπόδιζαν;

---

## 📊 Expected Timeline

- **Reconnaissance**: 5 λεπτά
- **Setup**: 10 λεπτά
- **Attack execution**: 5 λεπτά
- **Capture & verify**: 5 λεπτά
- **Cleanup**: 5 λεπτά

**Total**: ~30 λεπτά

---

## 🎓 What You Learned

✅ Πώς λειτουργεί το ARP protocol
✅ Πώς να κάνεις network reconnaissance
✅ Πώς να γίνεις MITM με ARP spoofing
✅ Πώς να forward traffic (IP forwarding)
✅ Γιατί χρειάζεται proper cleanup

---

## 🚀 Next Challenge

Έτοιμος για το **Hard challenge**? 🔴

Θα πρέπει να:
- Bypass HTTPS protections
- Perform SSL stripping
- Inject malicious JavaScript
- NO hints provided!

Go to: `../03-hard/`

---

**Great job completing the Medium challenge! 🎉**

You're now ready for advanced MITM techniques!

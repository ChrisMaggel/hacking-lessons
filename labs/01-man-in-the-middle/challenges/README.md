# 🎮 MITM Attack Challenges

Καλώς ήρθες στο **hands-on challenge section**! Εδώ θα εξασκηθείς σε πραγματικά MITM attacks.

---

## 📊 Challenge Overview

| Challenge | Difficulty | Time | Skills Required |
|-----------|-----------|------|-----------------|
| **01-easy** | 🟢 Beginner | 15 min | Packet sniffing, basic networking |
| **02-medium** | 🟡 Intermediate | 30 min | ARP spoofing, network recon, MITM positioning |
| **03-hard** | 🔴 Advanced | 1-2 hrs | SSL stripping, content injection, session hijacking |

---

## 🎯 Challenge Descriptions

### 🟢 Challenge 1: HTTP Credential Sniffing

**What you'll do**:
- Capture HTTP login credentials using packet sniffing
- Analyze plaintext traffic
- Extract usernames and passwords

**What you'll learn**:
- Why HTTP is insecure
- How packet sniffing works
- Using Scapy for network analysis

**Prerequisites**:
- Basic understanding of HTTP
- Comfortable with terminal

**Start here**: [`01-easy/README.md`](01-easy/README.md)

---

### 🟡 Challenge 2: ARP Poisoning Attack

**What you'll do**:
- Position yourself as MITM using ARP spoofing
- Intercept traffic between victim and gateway
- Capture real network traffic

**What you'll learn**:
- How ARP protocol works
- Network reconnaissance
- IP forwarding
- Proper attack cleanup

**Prerequisites**:
- Completed Easy challenge
- Understanding of IP/MAC addressing
- Access to test network or VMs

**Start here**: [`02-medium/README.md`](02-medium/README.md)

---

### 🔴 Challenge 3: HTTPS Downgrade & Content Injection

**What you'll do**:
- Strip SSL encryption (HTTPS → HTTP)
- Inject malicious JavaScript
- Hijack user sessions
- Evade detection mechanisms

**What you'll learn**:
- SSL/TLS attacks
- HSTS bypass techniques
- Content injection
- Session hijacking
- Operational security

**Prerequisites**:
- Completed Medium challenge
- Strong understanding of HTTP/HTTPS
- Familiar with SSL/TLS concepts
- Research skills (minimal guidance provided!)

**Start here**: [`03-hard/README.md`](03-hard/README.md)

---

## 🏆 Progression Path

```
START HERE
    ↓
┌─────────────┐
│ 🟢 EASY     │  ← Learn the basics
│ Credential  │     Packet sniffing
│ Sniffing    │     HTTP analysis
└──────┬──────┘
       ↓
┌─────────────┐
│ 🟡 MEDIUM   │  ← Become MITM
│ ARP         │     Network positioning
│ Spoofing    │     Traffic interception
└──────┬──────┘
       ↓
┌─────────────┐
│ 🔴 HARD     │  ← Master advanced attacks
│ SSL Strip & │     Encryption bypass
│ Injection   │     Stealth techniques
└─────────────┘
       ↓
   🎓 EXPERT
```

---

## ✅ How to Track Your Progress

After completing each challenge, mark it here:

- [ ] 🟢 **Easy Challenge** - HTTP Credential Sniffing
  - [ ] Captured 3+ credentials
  - [ ] Understand why HTTP is vulnerable
  - [ ] Can explain how packet sniffing works

- [ ] 🟡 **Medium Challenge** - ARP Poisoning
  - [ ] Successfully poisoned ARP cache
  - [ ] Victim's traffic flows through attacker
  - [ ] Properly restored network after attack

- [ ] 🔴 **Hard Challenge** - SSL Stripping & Injection
  - [ ] Successfully stripped SSL
  - [ ] Injected JavaScript in victim's browser
  - [ ] Captured session cookies

---

## 📝 General Tips

### Before Starting:

1. **Read the theory first**
   - Go through `../README.md` for background
   - Understand the attack before executing it

2. **Setup your environment**
   - VMs or isolated network
   - All required tools installed
   - Backups of important data

3. **Document everything**
   - Take screenshots
   - Save command outputs
   - Write notes on what works/doesn't work

### During Challenges:

1. **Read carefully**
   - Don't skip instructions
   - Understand each step before executing

2. **Use hints wisely**
   - Try on your own first
   - Only use hints when truly stuck
   - Learn from mistakes

3. **Experiment**
   - Try variations
   - Break things (in your lab!)
   - See what happens when you change parameters

### After Completion:

1. **Clean up**
   - Restore all systems
   - Delete captured credentials
   - Reset network settings

2. **Reflect**
   - What did you learn?
   - What was challenging?
   - How would you defend against this?

3. **Document**
   - Write a brief report
   - Include screenshots
   - Explain what you did

---

## 🛠️ Required Tools

### All Challenges:
- Python 3.7+
- Scapy (`pip install scapy`)
- Root/Admin privileges

### Medium Challenge:
- nmap (optional but helpful)
- Multiple machines/VMs

### Hard Challenge:
- mitmproxy or sslstrip
- bettercap (optional)
- More research required!

---

## ⚠️ Safety Guidelines

### DO:
✅ Use ONLY in isolated lab environments
✅ Get written permission for any real network testing
✅ Clean up after attacks (restore ARP tables, etc.)
✅ Document your learning
✅ Practice ethical hacking

### DON'T:
❌ Attack real users without permission
❌ Use on production networks
❌ Leave systems in broken state
❌ Keep captured credentials
❌ Forget about legal consequences

---

## 🆘 Getting Help

### If You're Stuck:

1. **Re-read the instructions**
   - Did you miss a step?
   - Are there hints you haven't checked?

2. **Check the main README**
   - `../README.md` has theory
   - `../exploit/README.md` has tool documentation
   - `../defense/README.md` has security context

3. **Debug systematically**
   - What's the exact error?
   - What did you expect vs what happened?
   - Can you isolate the problem?

4. **Research**
   - Google the error message
   - Check tool documentation
   - Read security blogs

### Common Issues:

**"Permission denied"**
→ Run with `sudo` (Linux/Mac) or as Administrator (Windows)

**"Module not found"**
→ Install required packages: `pip install scapy requests`

**"Network unreachable"**
→ Check if you're on the same network as targets

**"Can't capture packets"**
→ Verify interface name in scripts (eth0, wlan0, etc.)

---

## 📚 Learning Resources

### Before Challenges:
- **Networking Basics**: OSI model, TCP/IP, ARP
- **HTTP Protocol**: Request/response, headers, methods
- **Python Basics**: Enough to read and modify scripts

### During Challenges:
- **Scapy Documentation**: https://scapy.readthedocs.io/
- **Wireshark**: For packet analysis
- **RFC 826**: ARP protocol specification

### After Challenges:
- **OWASP**: Web security testing guide
- **Books**: "Web Application Hacker's Handbook"
- **Practice**: HackTheBox, TryHackMe

---

## 🎯 Challenge Goals

### Technical Skills:
- [x] Network packet analysis
- [x] ARP protocol manipulation
- [x] MITM positioning
- [x] Traffic interception
- [x] Content injection
- [x] Session hijacking

### Security Knowledge:
- [x] Why encryption matters
- [x] How MITM attacks work
- [x] Common vulnerabilities
- [x] Defense mechanisms
- [x] Detection methods

### Professional Skills:
- [x] Systematic debugging
- [x] Research abilities
- [x] Documentation
- [x] Ethical considerations
- [x] Clean operations

---

## 🏅 Certification

When you complete all 3 challenges:

1. **Create a portfolio**
   - Screenshots of successful attacks
   - Written explanations
   - Defense recommendations

2. **Write a report**
   - Executive summary
   - Technical details
   - Lessons learned
   - Mitigation strategies

3. **Share your knowledge**
   - Teach someone else
   - Write a blog post
   - Present at a meetup

---

## 🚀 What's Next?

After mastering MITM attacks, explore:

1. **Other Attack Categories**
   - SQL Injection
   - XSS (Cross-Site Scripting)
   - CSRF
   - etc.

2. **Advanced Topics**
   - Wireless hacking
   - Mobile app security
   - Cloud security
   - Binary exploitation

3. **Certifications**
   - CEH (Certified Ethical Hacker)
   - OSCP (Offensive Security Certified Professional)
   - GPEN (GIAC Penetration Tester)

---

**Ready to begin? Start with Challenge 1!** 🚀

Go to: [`01-easy/README.md`](01-easy/README.md)

---

**Good luck, and happy hacking (ethically)!** 🎭

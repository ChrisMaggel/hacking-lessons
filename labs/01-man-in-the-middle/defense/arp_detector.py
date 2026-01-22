#!/usr/bin/env python3
"""
========================================
ARP SPOOFING DETECTOR
========================================
This tool detects ARP spoofing attacks on your network.

HOW IT WORKS:
1. Monitors ARP traffic
2. Maintains a table of IP→MAC mappings
3. Alerts when a MAC address changes for an IP
4. Detects ARP floods (sign of attack)

DETECTION METHODS:
- Duplicate IP detection
- MAC address changes
- Gratuitous ARP monitoring
- ARP reply rate analysis

⚠️ Run with root/sudo privileges ⚠️
========================================
"""

from scapy.all import sniff, ARP, get_if_hwaddr
import time
from collections import defaultdict
from datetime import datetime

# ========================================
# CONFIGURATION
# ========================================
INTERFACE = "eth0"  # Network interface to monitor
ALERT_THRESHOLD = 10  # ARP packets/second threshold

# ========================================
# ARP TABLE - LEGITIMATE MAPPINGS
# ========================================
# Stores the "known good" IP→MAC mappings
arp_table = {}

# ========================================
# STATISTICS
# ========================================
arp_packet_count = defaultdict(int)  # Count ARP packets per IP
last_check_time = time.time()

# ========================================
# COLOR CODES
# ========================================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ========================================
# STEP 1: DETECT ARP SPOOFING
# ========================================
def detect_arp_spoofing(packet):
    """
    Analyze ARP packet for signs of spoofing.

    Detection methods:
    1. MAC address change for known IP
    2. Gratuitous ARP (sender IP = target IP)
    3. Duplicate IP announcements

    Args:
        packet: Scapy ARP packet
    """
    global arp_table, arp_packet_count, last_check_time

    # ========================================
    # EXTRACT ARP PACKET INFO
    # ========================================
    if packet.haslayer(ARP):
        arp = packet[ARP]

        src_ip = arp.psrc  # Source IP
        src_mac = arp.hwsrc  # Source MAC
        dst_ip = arp.pdst  # Destination IP
        op = arp.op  # Operation: 1=request, 2=reply

        timestamp = datetime.now().strftime("%H:%M:%S")

        # ========================================
        # DETECTION 1: MAC ADDRESS CHANGE
        # ========================================
        if src_ip in arp_table:
            # We've seen this IP before
            known_mac = arp_table[src_ip]

            if known_mac != src_mac:
                # ⚠️ MAC address changed for this IP!
                print(f"\n{Colors.RED}{'='*60}{Colors.RESET}")
                print(f"{Colors.RED}{Colors.BOLD}🚨 ARP SPOOFING DETECTED! 🚨{Colors.RESET}")
                print(f"{Colors.RED}{'='*60}{Colors.RESET}")
                print(f"Time:     {timestamp}")
                print(f"IP:       {Colors.YELLOW}{src_ip}{Colors.RESET}")
                print(f"Old MAC:  {Colors.GREEN}{known_mac}{Colors.RESET}")
                print(f"New MAC:  {Colors.RED}{src_mac}{Colors.RESET}")
                print(f"Type:     {'ARP Reply' if op == 2 else 'ARP Request'}")
                print(f"{Colors.RED}{'='*60}{Colors.RESET}\n")

                # Log the incident
                log_attack(timestamp, src_ip, known_mac, src_mac)

        else:
            # First time seeing this IP - add to table
            arp_table[src_ip] = src_mac
            print(f"[{timestamp}] {Colors.GREEN}New device:{Colors.RESET} {src_ip} → {src_mac}")

        # ========================================
        # DETECTION 2: GRATUITOUS ARP
        # ========================================
        # Gratuitous ARP = sender announces its own IP
        # Used by MITM attackers to poison caches
        if src_ip == dst_ip and op == 2:  # op=2 means ARP reply
            print(f"\n{Colors.YELLOW}{'='*60}{Colors.RESET}")
            print(f"{Colors.YELLOW}⚠️  GRATUITOUS ARP DETECTED{Colors.RESET}")
            print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}")
            print(f"Time:     {timestamp}")
            print(f"IP:       {src_ip}")
            print(f"MAC:      {src_mac}")
            print(f"Note:     Could be legitimate (IP change) or attack!")
            print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}\n")

        # ========================================
        # DETECTION 3: ARP FLOOD DETECTION
        # ========================================
        # Too many ARP packets = possible attack
        arp_packet_count[src_ip] += 1

        # Check every 5 seconds
        current_time = time.time()
        if current_time - last_check_time >= 5:
            detect_arp_flood()
            # Reset counters
            arp_packet_count.clear()
            last_check_time = current_time

# ========================================
# STEP 2: DETECT ARP FLOOD
# ========================================
def detect_arp_flood():
    """
    Detect if any IP is sending too many ARP packets.
    ARP flooding is a common MITM technique.
    """
    for ip, count in arp_packet_count.items():
        packets_per_second = count / 5.0

        if packets_per_second > ALERT_THRESHOLD:
            print(f"\n{Colors.RED}{'='*60}{Colors.RESET}")
            print(f"{Colors.RED}{Colors.BOLD}🚨 ARP FLOOD DETECTED! 🚨{Colors.RESET}")
            print(f"{Colors.RED}{'='*60}{Colors.RESET}")
            print(f"Source IP:  {ip}")
            print(f"Rate:       {packets_per_second:.1f} packets/second")
            print(f"Threshold:  {ALERT_THRESHOLD} packets/second")
            print(f"MAC:        {arp_table.get(ip, 'Unknown')}")
            print(f"{Colors.RED}{'='*60}{Colors.RESET}\n")

# ========================================
# STEP 3: LOG ATTACKS TO FILE
# ========================================
def log_attack(timestamp, ip, old_mac, new_mac):
    """
    Log detected attacks to a file for forensics.

    Args:
        timestamp: Time of detection
        ip: IP address involved
        old_mac: Previous MAC address
        new_mac: New (potentially spoofed) MAC address
    """
    try:
        with open("arp_attacks.log", "a") as f:
            f.write(f"[{timestamp}] ARP SPOOFING DETECTED\n")
            f.write(f"  IP:      {ip}\n")
            f.write(f"  Old MAC: {old_mac}\n")
            f.write(f"  New MAC: {new_mac}\n")
            f.write("-"*60 + "\n\n")

        print(f"{Colors.GREEN}[+] Attack logged to arp_attacks.log{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error logging attack: {e}{Colors.RESET}")

# ========================================
# STEP 4: DISPLAY ARP TABLE
# ========================================
def show_arp_table():
    """
    Display the current ARP table (known mappings).
    """
    print("\n" + "="*60)
    print("KNOWN ARP MAPPINGS")
    print("="*60)

    if arp_table:
        for ip, mac in sorted(arp_table.items()):
            print(f"{ip:20} → {mac}")
    else:
        print("No entries yet...")

    print("="*60 + "\n")

# ========================================
# STEP 5: START MONITORING
# ========================================
def start_monitoring(interface):
    """
    Start monitoring ARP traffic for spoofing attacks.

    Args:
        interface: Network interface to monitor
    """
    print("="*60)
    print("🕵️  ARP SPOOFING DETECTOR")
    print("="*60)
    print(f"[*] Interface: {interface}")
    print(f"[*] Monitoring ARP traffic...")
    print(f"[*] Flood threshold: {ALERT_THRESHOLD} packets/second")
    print(f"[*] Press Ctrl+C to stop and view summary")
    print("="*60)
    print()

    try:
        # ========================================
        # START PACKET CAPTURE
        # ========================================
        # filter="arp" → only capture ARP packets
        # prn=detect_arp_spoofing → call our function for each packet
        # store=0 → don't store packets (saves memory)
        sniff(
            iface=interface,
            filter="arp",
            prn=detect_arp_spoofing,
            store=0
        )

    except KeyboardInterrupt:
        print(f"\n\n{Colors.BLUE}[*] Monitoring stopped{Colors.RESET}")
        show_arp_table()
        print_statistics()

    except PermissionError:
        print(f"\n{Colors.RED}[-] Permission denied!{Colors.RESET}")
        print(f"{Colors.RED}[-] Run with: sudo python3 arp_detector.py{Colors.RESET}")

    except Exception as e:
        print(f"\n{Colors.RED}[-] Error: {e}{Colors.RESET}")

# ========================================
# STEP 6: STATISTICS
# ========================================
def print_statistics():
    """
    Print detection statistics.
    """
    print("\n" + "="*60)
    print("📊 STATISTICS")
    print("="*60)
    print(f"Total devices seen: {len(arp_table)}")

    # Check if log file exists
    import os
    if os.path.exists("arp_attacks.log"):
        with open("arp_attacks.log", "r") as f:
            attacks = f.read().count("ARP SPOOFING DETECTED")
        print(f"Attacks detected:   {attacks}")
        print(f"Log file:           arp_attacks.log")
    else:
        print(f"Attacks detected:   0")

    print("="*60 + "\n")

# ========================================
# MAIN FUNCTION
# ========================================
def main():
    """
    Main entry point.
    """
    import os

    # Check for root privileges
    if os.geteuid() != 0:
        print(f"{Colors.RED}[-] This script requires root privileges{Colors.RESET}")
        print(f"{Colors.RED}[-] Run with: sudo python3 arp_detector.py{Colors.RESET}")
        return

    start_monitoring(INTERFACE)

if __name__ == "__main__":
    main()

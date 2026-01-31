Automated Network Scanner & Logger
 Overview
A Python-based network reconnaissance tool designed to map a local area network (LAN) and log active devices. By leveraging Scapy for low-level packet crafting, the script identifies connected devices via ARP requests and performs vendor identification using a hybrid approach (local OUI database + REST API).

This project was developed to bridge the gap between theoretical networking concepts (OSI Model, ARP protocol) and practical Python automation.

 Features
Layer 2 Scanning: Uses ARP (Address Resolution Protocol) to discover devices, making it more reliable than standard ICMP pings.

Hybrid Vendor Identification: Matches MAC addresses against a local mac_database.txt for speed and utilizes the MacVendors REST API for unknown devices.

Automated Logging: Exports scan results to a structured CSV file with timestamps for historical network monitoring.

Data Enrichment: Utilizes Pandas to organize IP addresses, MAC addresses, and Hardware Vendors into a clean tabular format.

 Tech Stack
Language: Python 3.x

Libraries: * Scapy: Packet crafting and network communication.

Pandas: Data manipulation and CSV export.

Requests: Handling API calls for vendor lookup.

Drivers: Npcap (Windows packet capture driver).

How It Works
Encapsulation: The script creates an Ethernet frame addressed to the broadcast MAC (ff:ff:ff:ff:ff:ff) and nests an ARP request inside it using the Scapy / operator.

Transmission: The packet is broadcast across the specified subnet (e.g., 192.168.3.0/24).

Collection: The script listens for ARP replies, extracting the psrc (IP) and hwsrc (MAC) from each responding device.

Enrichment & Storage: Each MAC is checked against the OUI database to identify the manufacturer (e.g., Samsung, Apple, TP-Link) and saved to a CSV log.

 Getting Started:
Install Npcap on Windows (ensure "WinPcap compatibility mode" is checked).

Install dependencies:

Bash
pip install scapy pandas requests
Run with administrative privileges:

Bash
python network_scanner.py

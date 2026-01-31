from sys import prefix
import ipaddress
import requests
import time
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import pandas as pd


def scan_my_network(ip_range):

    # Ether creates the frame for the hardware (MAC) level
    # ARP creates the request for the protocol (IP) level
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)



    # I used [0] to grab only the answered responses
    print(f"Scanning {ip_range}... please wait.")
    answered_list = srp(packet, timeout=5, verbose=False)[0]


    # I create a list of dictionaries
    clients = []
    for sent, received in answered_list:
        ip =received.psrc
        mac = received.hwsrc
        vendor = lookup_vendor_local(mac)
        if vendor == "unknown":
            print(f"Checking API for {mac}...")
            vendor= looup_vendor_api(mac)
        clients.append({
            "IP Address": ip,
            "MAC Address": mac,
            "vendor": vendor
        })

    return clients
#this looks up the vendors from a local text file for faster lookup time
#if its not there it will make an api request
def lookup_vendor_local(mac_address):
    prefix=mac_address[:8].lower()
    try:
        with open("mac_database.txt", "r") as f:
            for line in f:
                stored_address,vendor=line.strip().split(",")
                if stored_address.lower() == prefix:
                    return vendor
    except FileNotFoundError:
        return "file not found"
    return "unknown"
def looup_vendor_api(mac_address):
    time.sleep(1)
    url = f"https://api.macvendors.com/{mac_address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "vendor not found"
    except Exception as e:
        return "connection error"

#this function checks if the entered ip is valid
def get_valid_ip():
    while True:
        user_input = input("Enter the IP range to scan (e.g., 192.168.1.1/24): ")
        try:

            network = ipaddress.ip_network(user_input, strict=False)
            return str(network)
        except ValueError:
            print(" Invalid IP address or range. Please try again.")
# --- Main Execution Block ---
if __name__ == "__main__":
    
    target_range = get_valid_ip()


    found_devices = scan_my_network(target_range)


    # This turns the list of dictionaries into a professional table
    df = pd.DataFrame(found_devices)

    if not df.empty:
        print("\nDevices found on your network:")
        print(df)
        # Saves the result to a csv file in the project folder
        df.to_csv("network_report.csv", index=False)
    else:

        print("No devices found. Check your IP range!")

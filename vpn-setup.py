import os
import subprocess
import time
import random

def generate_random_ip():
    # Generate a random IP address in the range 10.8.0.0 to 10.8.255.255
    return f"10.8.{random.randint(0, 255)}.{random.randint(0, 255)}"

def install_openvpn():
    # Install OpenVPN
    os.system("apt-get update && apt-get install -y openvpn")

def configure_openvpn():
    # Initialize OpenVPN server configuration
    os.system("openvpn --genkey --secret /etc/openvpn/server.key")

    # Generate a random IP address for the virtual IP pool
    virtual_ip_pool = generate_random_ip()

    # Create OpenVPN server configuration file
    server_conf = f"""
    port 1194
    proto udp
    dev tun
    ca /etc/openvpn/server.crt
    cert /etc/openvpn/server.crt
    key /etc/openvpn/server.key  # Use the key generated earlier
    dh /etc/openvpn/dh2048.pem
    server {virtual_ip_pool} 255.255.255.0
    ifconfig-pool-persist ipp.txt
    push "redirect-gateway def1 bypass-dhcp"
    push "dhcp-option DNS 8.8.8.8"
    keepalive 10 120
    cipher AES-256-CBC
    comp-lzo
    max-clients 10
    user nobody
    group nogroup
    persist-key
    persist-tun
    status /var/log/openvpn-status.log
    verb 3
    """

    with open("/etc/openvpn/server.conf", "w") as f:
        f.write(server_conf)

def start_openvpn():
    # Start OpenVPN service
    os.system("service openvpn start")

def monitor_openvpn():
    # Monitor OpenVPN service status every 10 seconds
    while True:
        status = subprocess.getoutput("service openvpn status")
        print("OpenVPN Status:")
        print(status)
        time.sleep(10)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script as root.")
    else:
        # Install OpenVPN
        install_openvpn()

        # Configure OpenVPN
        configure_openvpn()

        # Start OpenVPN service
        start_openvpn()

        # Monitor OpenVPN service
        monitor_openvpn()

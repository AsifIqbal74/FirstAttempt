import socket
import subprocess
import platform

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def scan_network(ip):
    ip_parts = ip.split('.')
    base_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
    
    active_ips = []
    
    for i in range(1, 255):
        target_ip = f"{base_ip}.{i}"
        if platform.system().lower() == "windows":
            command = ['ping', '-n', '1', '-w', '500', target_ip]
        else:
            command = ['ping', '-c', '1', '-W', '1', target_ip]
        
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            if "TTL=" in output or "ttl=" in output:
                active_ips.append(target_ip)
        except subprocess.CalledProcessError:
            pass
    
    return active_ips

local_ip = get_local_ip()
print(f"Your IP: {local_ip}")
print("Scanning network for active IP addresses...")
active_ips = scan_network(local_ip)

print("\nActive IP addresses on the network:")
for ip in active_ips:
    print(ip)
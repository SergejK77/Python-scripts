import scapy.all as scapy
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def scan_network(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    active_devices = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    devices = []
    for element in active_devices:
        device_info = {
            "ip": element[1].psrc,
            "mac": element[1].hwsrc
        }
        devices.append(device_info)

    return devices


if __name__ == "__main__":
    ip_address = get_ip()
    ip_range = ip_address.rsplit('.', 1)[0] + '.1/24'
    print(f"Scanning network: {ip_range} ...")
    devices = scan_network(ip_range)
    if devices:
        print(devices)
    else:
        print("No devices found.")

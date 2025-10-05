import socket
from termcolor import colored


def scan(target, ports):
    print(f'\n' + f'*** Starting Scan for: {target}***')
    for port in range(97, ports):
        scan_port(target, port)


def get_banner(s):
    return s.recv(1024)


def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.4)
        sock.connect((ipaddress, port))
        svc = socket.getservbyport(port, "tcp")
        try:
            banner = get_banner(sock)
            print(f'[*] Open Port {port} // {banner} // {svc}')
        except:
            print(f'[*] Open Port {port} // {svc} ')
        sock.close()
    except:
        pass


targets = input('Enter target IP:')
ports = int(input('Enter target ports:'))
if ',' in targets:
    print(colored(("\n Scanning multiple Targets [*] \n"), 'green'))
    for ip_add in targets.split(','):
        scan(ip_add.strip(' '), ports)
else:
    scan(targets, ports)
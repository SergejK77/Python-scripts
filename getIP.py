import requests

ipv6 = requests.get("https://api64.ipify.org?format=json").json()["ip"]
ipv4 = requests.get("https://api.ipify.org?format=json").json()["ip"]
print(f"My public IPv6 is: {ipv6}")
print(f"My public IPv4 is: {ipv4}")

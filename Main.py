import sys
from DnsClient import DnsClient

main_root_server = '192.33.4.12'
reserved_root_server = '8.8.8.8'
port = 53
dns_client = DnsClient('UDP',True)
try:
    print(dns_client.get_ip('e1.com', main_root_server, port))
except (ValueError, TimeoutError):
    print(dns_client.get_ip('e1.com', reserved_root_server, port))

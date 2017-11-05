import sys
from DnsClient import DnsClient

root_server_ip = '192.33.4.12'
google_sever_ip = '8.8.8.8'

dns_client = DnsClient('UDP')
print(dns_client.get_ip('quora.com', root_server_ip))

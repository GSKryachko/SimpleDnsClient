import sys
from DnsClient import DnsClient
from PackageTypeEnums import package_type

main_root_server = '192.33.4.12'
reserved_root_server = '8.8.8.8'
port = 53
dns_client = DnsClient('UDP', False)
try:
    print(dns_client.get_ip('e1.ru', main_root_server, req_type=package_type.NS, port=port))
except (ValueError, TimeoutError) as e:
    print(e)
    print(dns_client.get_ip('e1.ru', reserved_root_server, req_type=package_type.NS, port=port))

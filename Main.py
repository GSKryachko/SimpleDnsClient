from DnsClient import DnsClient
from PackageTypeEnums import package_type
import argparse

parser = argparse.ArgumentParser(description='Returns address or cname by site name')
parser.add_argument('site_name', metavar='site name', type=str,
                    help='site name')
parser.add_argument('protocol', metavar='transport protocol', type=str,
                    help='can be either tcp or udp')
parser.add_argument('port', metavar='port', default=53,
                    help='DNS server port. Default value is 53, in accordance with RFC')
parser.add_argument('main_root_server', metavar='root server ip', type=str,
                    help='root server ip')
parser.add_argument('reserved_root_server', metavar='reserved server ip', type=str,
                    help='reserved server ip, will be used only if some problem '
                         'will occur with first root server')

parser.add_argument('pack_type', metavar='desired answer type', type=str,
                    default=package_type.A)

parser.add_argument('recurrent_queries', metavar='')

args = parser.parse_args()
main_root_server = '192.33.4.12'
reserved_root_server = '8.8.8.8'
port = 53
address = 'quora.com'
req_type = package_type.A
dns_client = DnsClient(args.protocol.upper, True)
try:
    print(dns_client.get_ip(address, main_root_server, req_type=req_type, port=port))
except (ValueError, TimeoutError) as e:
    print(dns_client.get_ip(address, reserved_root_server, req_type=req_type, port=port))

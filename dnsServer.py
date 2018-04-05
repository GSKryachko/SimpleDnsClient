from dnslib import *

from PackageEncoder import *
from dnsClient import DnsClient
from packageParser import PackageParser

if __name__ == '__main__':
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.bind(('localhost', 53))
    client = DnsClient()
    resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns = ('8.8.8.8', 53)
    while True:
        data, addr = listener.recvfrom(1024)
        resolver.sendto(data, dns)
        resp = resolver.recv(1024)
        package_parser = PackageParser()
        package_parser.parse_response(resp)
        dns_package = package_parser.get_dns_package()
        reconstructed = encode_package(dns_package)
        listener.sendto(reconstructed, addr)

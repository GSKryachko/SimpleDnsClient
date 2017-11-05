import socket
from PackageTypeEnums import package_type

import struct


class RequestHandler:
    def __init__(self, protocol):
        if protocol not in ['TCP', 'UDP']:
            raise ValueError('Protocol should be either TCP or UDP')
        self.protocol = protocol
    
    def send_request(self, address, dns_sever_ip, dns_server_port, recursive=False):
        request = self.create_request(address, recursive=recursive)
        if self.protocol == 'UDP':
            return self.send_via_udp(request, dns_sever_ip, dns_server_port)
        if self.protocol == 'TCP':
            return self.send_via_tcp(request, dns_sever_ip, dns_server_port)
        raise ValueError('Protocol should be either TCP or UDP')
    
    def send_via_udp(self, request, dns_sever_ip, dns_server_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.setdefaulttimeout(10)
        s.sendto(request, (dns_sever_ip, dns_server_port))
        res = s.recv(1024)
        print(len(res))
        return res
    
    def send_via_tcp(self, request, dns_server_ip, dns_server_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((dns_server_ip, dns_server_port))
        s.sendall(request)
        res = s.recv(2 ** 16)
        s.close()
        return res
    
    def create_request(self, address, req_type=package_type.A, req_class='IN', recursive=True):
        dns = b''
        dns += b'\xAB\xCD'  # transaction id
        flag = 0
        flag += int(recursive)
        flag *= 2 ** 8
        dns += flag.to_bytes(2, 'big')
        dns += (1).to_bytes(2, 'big')  # questions
        dns += (0).to_bytes(2, 'big')  # responses
        dns += (0).to_bytes(2, 'big')  # authority resource records
        dns += (0).to_bytes(2, 'big')  # additional resource records
        
        dns += self.encode_address_with_hex_prefixes(address)
        dns += req_type.value
        if req_class == 'IN':
            dns += ((1).to_bytes(2, 'big'))
        return dns
    
    def encode_address_with_hex_prefixes(self, address):
        ans = b''
        for word in address.split('.'):
            ans += bytes([len(word)]) + word.encode('ASCII')
        ans += b'\x00'
        return ans

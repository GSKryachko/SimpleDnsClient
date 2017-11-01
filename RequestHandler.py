import socket
from PackageTypeEnums import package_type
import struct


class RequestHandler:
    def send_request(self, address, dns_sever_ip, dns_server_port, recursive=False):
        request = self.create_request(address, recursive=recursive)
        print(request)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.setdefaulttimeout(10)
        s.sendto(request, (dns_sever_ip, dns_server_port))
        res = s.recv(1024)
        print(res)
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

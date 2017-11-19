import socket

import struct


class NetworkManager:
    def __init__(self, protocol):
        if protocol not in ['TCP', 'UDP']:
            raise ValueError('Protocol should be either TCP or UDP')
        self.protocol = protocol
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) if protocol == 'UDP'\
            else socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def send(self, request, dns_server_ip, dns_server_port):
        if self.protocol == 'UDP':
            return self.send_via_udp(request, dns_server_ip, dns_server_port)
        else:
            return self.send_via_tcp(request, dns_server_ip, dns_server_port)
    
    def send_via_udp(self, request, dns_server_ip, dns_server_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.setdefaulttimeout(100)
        s.sendto(request, (dns_server_ip, dns_server_port))
        res = s.recv(1024)
        return res
    
    def send_via_tcp(self, request, dns_server_ip, dns_server_port):
        request = struct.pack("!H", len(request)) + request
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((dns_server_ip, dns_server_port))
        sock.sendall(request)
        response = sock.recv(8192)
        length = struct.unpack("!H", bytes(response[:2]))[0]
        while len(response) - 2 < length:
            response += sock.recv(8192)
        sock.close()
        response = response[2:]
        return response

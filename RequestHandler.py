import socket

import struct


def send_request(address, dns_sever_ip, dns_server_port, recursive=False):
    request = create_request(address, recursive=recursive)
    print(request)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    socket.setdefaulttimeout(10)
    #s.connect((dns_sever_ip, int(dns_server_port)))
    s.sendto(request, (dns_sever_ip,dns_server_port))
    res = s.recv(1024)
    print(res)


def create_request(address, req_type='A', req_class='IN', recursive=False):
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
    
    dns += encode_address_with_hex_prefixes(address)
    if req_type == 'A':
        dns += ((1).to_bytes(2, 'big'))
    if req_class == 'IN':
        dns += ((1).to_bytes(2, 'big'))
    return dns


def encode_address_with_hex_prefixes(address):
    ans = b''
    for word in address.split('.'):
        ans += bytes([len(word)]) + word.encode('ASCII')
    ans += b'\x00'
    return ans

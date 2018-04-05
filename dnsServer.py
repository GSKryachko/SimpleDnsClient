from dnslib import *
from responseHandler import ResponseHandler
from dnsClient import DnsClient

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
        response_handler = ResponseHandler()
        response_handler.parse_response(resp)
        listener.sendto(resp, addr)

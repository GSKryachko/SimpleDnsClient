from DnsClient import DnsClient
from MySock import MySocket
from RequestHandler import *
import http
import io
from ResponseHandler import ResponseHandler

root_server_ip = '192.33.4.12'
next_sever_ip ='194.85.252.62'
hex_string = '7a65010000010000000000000377777706676f6f676c6503636f6d0000010001'.encode()

dns_client = DnsClient()
next_address = root_server_ip
print(dns_client.get_ip('forbes.com',root_server_ip))
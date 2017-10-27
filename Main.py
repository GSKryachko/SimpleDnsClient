from MySock import MySocket
from RequestHandler import *
import http
root_server_ip = '192.33.4.12'
hex_string = '7a65010000010000000000000377777706676f6f676c6503636f6d0000010001'
resp = bytearray.fromhex(hex_string)
send_request('www.google.com',root_server_ip,53,False)
# import urllib.request
# response = urllib.request.urlopen('http://python.org/')
# html = response.read()
# print(html)
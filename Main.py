from MySock import MySocket
from RequestHandler import *
import http
import io
from ResponseHandler import ResponseHandler

root_server_ip = '192.33.4.12'
next_sever_ip ='194.85.252.62'
hex_string = '7a65010000010000000000000377777706676f6f676c6503636f6d0000010001'.encode()


resp = send_request('google.ru', next_sever_ip, 53, False)
response_handler = ResponseHandler()
response_handler.parse_response(resp)

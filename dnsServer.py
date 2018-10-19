import sys
import threading

from dnslib import *

from packageEncoder import *
from packageParser import *
from serverCash import Cash
import json

class DnsServer:
    def __init__(self):
        with open('config.json','r') as f:
            config = json.load(f)
        self.cash = Cash()
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(('localhost', 53))
        self.resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dns = (config['main_server_ip'], 53)
        self.cash.load()
        self.resolver.settimeout(5)
        self.cleaner = threading.Thread(target=self.cash.assure_consistency,name='cleaner')
        self.cleaner.setDaemon(True)
        self.cleaner.start()
        self.waiter = threading.Thread(target=self.wait_for_termination,name='waiter')
        self.waiter.setDaemon(True)
        self.waiter.start()
    
    def request_and_save_answer_from_server(self, question):
        try:
            self.resolver.sendto(question, self.dns)
            resp = self.resolver.recv(1024)
            
            dns_package = parse_response(resp)
            self.cash.register_package(dns_package)
            return resp
        except Exception as e:
            return None
    
    def run(self):
        while self.waiter.isAlive():
            data, addr = self.listener.recvfrom(1024)
            dns_package = parse_response(data)
            question = dns_package.questions[0]
            answer = self.cash.get_answer(question)
            if answer:
                dns_package.add_answer(answer)
                response = encode_package(dns_package)
                print('That was an answer from cash')
                self.cash.print()
                self.listener.sendto(response, addr)
                continue
            else:
                response = self.request_and_save_answer_from_server(data)
                if response:
                    self.listener.sendto(response, addr)
                else:
                    print("Other server didn't respond")
        self.cash.save()
        print('Main loop has ended')
        for thread in threading.enumerate():
            print(thread)
        sys.exit(0)
        
    def wait_for_termination(self):
        while True:
            if input(':') == 'exit':
                print('Waiting for one more package before terminating')
                return
            else:
                print("Print 'exit' to terminate server")


if __name__ == '__main__':
    DnsServer().run()

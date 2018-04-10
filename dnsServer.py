from dnslib import *

from packageParser import PackageParser
from serverCash import Cash
from PackageEncoder import *

class DnsServer:
    def __init__(self):
        self.cash = Cash()
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(('localhost', 53))
        self.resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dns = ('8.8.8.8', 53)
    
    def form_response_from_cash(self, question):
        question.answers.append(
            self.cash.name_to_data[question.questions[0].name])
        return encode_package(question)
    
    def request_and_save_answer_from_server(self, question):
        self.resolver.sendto(question, self.dns)
        resp = self.resolver.recv(1024)
        package_parser = PackageParser()
        package_parser.parse_response(resp)
        dns_package = package_parser.get_dns_package()
        self.cash.register_package(dns_package)
        return resp
    
    def run(self):
        while True:
            data, addr = self.listener.recvfrom(1024)
            # self.resolver.sendto(data, self.dns)
            # resp = self.resolver.recv(1024)
            
            package_parser = PackageParser()
            package_parser.parse_response(data)
            dns_package = package_parser.get_dns_package()
            
            name = dns_package.questions[0].name
            if name in self.cash.name_to_data:
                response = self.form_response_from_cash(dns_package)
                print('That was an answer from cash')
            else:
                response = self.request_and_save_answer_from_server(data)
            
            self.listener.sendto(response, addr)


if __name__ == '__main__':
    DnsServer().run()

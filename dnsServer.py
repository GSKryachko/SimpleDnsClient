from dnslib import *

from packageEncoder import *
from packageParser import *
from serverCash import Cash


class DnsServer:
    def __init__(self):
        self.cash = Cash()
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(('localhost', 53))
        self.resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dns = ('8.8.8.8', 53)
        self.alive = True
        self.cash.load()
        self.resolver.settimeout(5)
        # cleaner = threading.Thread(target=self.cash.assure_consistency)
        # cleaner.deamon = True
        #
        # threading.Thread(target=self.wait_for_termination).start()
    
    def request_and_save_answer_from_server(self, question):
        try:
            self.resolver.sendto(question, self.dns)
            resp = self.resolver.recv(1024)
            
            dns_package = parse_response(resp)
            if dns_package.questions:
                print("registering package...")
            self.cash.register_package(dns_package)
            return resp
        except Exception as e:
            raise
    
    def run(self):
        while self.alive:
            data, addr = self.listener.recvfrom(1024)
            # self.resolver.sendto(data, self.dns)
            # resp = self.resolver.recv(1024)
            #
            # package_parser = PackageParser()
            # package_parser.parse_response(data)
            dns_package = parse_response(data)
            
            print(*[(x.name, x.type) for x in dns_package.questions])
            print(self.cash.a)
            print(self.cash.ns)
            
            question = dns_package.questions[0]
            answer = self.cash.get_answer(question)
            if answer:
                dns_package.answers.append(answer)
                response = encode_package(dns_package)
                print('That was an answer from cash')
                self.listener.sendto(response, addr)
                continue
            else:
                try:
                    response = self.request_and_save_answer_from_server(data)
                    self.listener.sendto(response, addr)
                except Exception as e:
                    raise
                    print("Other server didn't respond")
        self.cash.save()
    
    def wait_for_termination(self):
        while True:
            if input(':') == 'exit':
                self.alive = False
                return
            else:
                print("Print 'exit' to terminate server")


if __name__ == '__main__':
    DnsServer().run()

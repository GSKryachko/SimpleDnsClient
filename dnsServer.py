from queryResolver import QueryResolver
from packageTypeEnums import PackageType
import re


class DnsServer:
    def __init__(self):
        self.main_root_server = '192.33.4.12'
        self.reserved_root_server = '8.8.8.8'
        self.port = 53
        self.address = None
        self.req_type = PackageType.A
        self.protocol = 'UDP'
        self.extractor = re.compile(r'.*=\s*(.*)\s*')
        self.recursion = True
    
    def run(self):
        self.print_help()
        while self.parse_command(input(">")) != 'exit':
            pass
    
    def extract_value(self, command):
        return re.search(self.extractor, command).group(1)
    
    def get_address(self):
        dns_client = QueryResolver(self.protocol, self.recursion)
        try:
            print(dns_client.get_ip(self.address, self.main_root_server,
                                    req_type=self.req_type, port=self.port))
        except (ValueError, TimeoutError) as e:
            print(dns_client.get_ip(self.address, self.reserved_root_server,
                                    req_type=self.req_type, port=self.port))
    
    @staticmethod
    def parse_bool(bool_as_string):
        if bool_as_string in ['True', 'true']:
            return True
        if bool_as_string in ['False', 'false']:
            return False
        raise ValueError(bool_as_string + ' is not bool')
    
    def parse_command(self, command):
        if command == 'exit':
            return 'exit'
        elif command in ['-h', '--help']:
            self.print_help()
        elif 'type' in command:
            self.req_type = PackageType.parse(self.extract_value(command)) or self.req_type
        elif 'protocol' in command:
            self.protocol = self.extract_value(command)
        elif 'main_server' in command:
            self.main_root_server = self.extract_value(command)
        elif 'reserved_server' in command:
            self.reserved_root_server = self.extract_value(command)
        elif 'port' in command:
            self.port = int(self.extract_value(command))
        elif 'recursion' in command:
            self.recursion = self.parse_bool(self.extract_value(command))
        else:
            try:
                self.address = command
                self.get_address()
            except ValueError:
                print("No results for: " + command)
                self.print_help()
    
    @staticmethod
    def print_help():
        help_str = "DNS server \n" \
                   "--help.-h help\n" \
                   "type=<dns package type> sets type\n" \
                   "port=<port> sets port\n" \
                   "recursion=<true/false> if true, server will request recursion\n" \
                   "main_server=<ip> sets main dns ip\n" \
                   "reserved_server=<ip> sets reserved server ip\n" \
                   "protocol=<TCP/UDP> sets transport protocol\n" \
                   "exit close program\n" \
                   "<address> returns data of address of type specified by type argument \n"
        print(help_str)


if __name__ == '__main__':
    console = DnsServer()
    console.run()

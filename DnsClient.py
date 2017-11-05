from ResponseHandler import ResponseHandler
from RequestHandler import RequestHandler
from PackageTypeEnums import package_type


class DnsClient():
    def __init__(self,protocol):
        self.response_handler = ResponseHandler()
        self.request_handler = RequestHandler(protocol)
    
    def get_next_resource_record(self, address, dns_server_ip):
        resp = self.request_handler.send_request(address, dns_server_ip, 53, False)
        self.response_handler.parse_response(resp)
        for answer in self.response_handler.answers:
            yield answer
        for answer in self.response_handler.additional:
            yield answer
        for answer in self.response_handler.authority:
            yield answer
    
    def get_ip(self, address, root_ip):
        if address is None:
            raise ValueError
        for answer in self.get_next_resource_record(address, root_ip):
            if answer.internal_type == 'answer':
                return answer.address
            if answer.internal_type == 'additional':
                if answer.type == package_type.A.value:
                    return self.get_ip(address, answer.address)
                return self.get_ip(address, self.get_ip(answer.address, root_ip))
            if answer.internal_type == 'authority':
                return self.get_ip(address, self.get_ip(answer.address, root_ip))

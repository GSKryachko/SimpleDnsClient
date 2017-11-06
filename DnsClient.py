from NetworkHandler import NetworkHandler
from ResponseHandler import ResponseHandler
from RequestHandler import RequestHandler
from PackageTypeEnums import package_type


class DnsClient():
    def __init__(self, protocol, support_resolving=True):
        self.response_handler = ResponseHandler()
        self.request_handler = RequestHandler(protocol)
        self.network_handler = NetworkHandler(protocol)
        self.support_resolving = support_resolving
    
    def get_next_resource_record(self, address, dns_server_ip, port=53):
        request = self.request_handler.create_request(address, self.support_resolving)
        resp = self.network_handler.send_via_udp(request, dns_server_ip, port)
        self.response_handler.parse_response(resp)
        for answer in self.response_handler.answers:
            yield answer
        for answer in self.response_handler.additional:
            yield answer
        for answer in self.response_handler.authority:
            yield answer
    
    def get_ip(self, address, root_ip, port=53):
        if address is None:
            raise ValueError
        for answer in self.get_next_resource_record(address, root_ip, port):
            if answer.internal_type == 'answer':
                return answer.address
            if answer.internal_type == 'additional':
                if answer.type == package_type.A.value or answer.type == package_type.AAAA.value:
                    return self.get_ip(address, answer.address)
                return self.get_ip(address, self.get_ip(answer.address, root_ip, port))
            if answer.internal_type == 'authority':
                return self.get_ip(address, self.get_ip(answer.address, root_ip, port))

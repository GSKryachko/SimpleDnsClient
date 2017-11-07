class DnsResourceRecord:
    def __init__(self, query_type, clas, ttl=None, address=None):
        self.type = query_type
        self.clas = clas
        self.ttl = ttl
        self.address = address

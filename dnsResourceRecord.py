class DnsResourceRecord:
    def __init__(self, query_type, clas, ttl=None, address=None, internal_type=None):
        self.type = query_type
        self.clas = clas
        self.ttl = ttl
        self.address = address
        self.internal_type = internal_type

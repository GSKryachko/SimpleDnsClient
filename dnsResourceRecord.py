class DnsResourceRecord:
    def __init__(self, query_type, clas, ttl=None, name=None, data=None,
                 internal_type=None):
        self.type = query_type
        self.clas = clas
        self.ttl = ttl
        self.name = name
        self.data = data
        self.internal_type = internal_type

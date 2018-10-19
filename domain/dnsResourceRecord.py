class DnsResourceRecord:
    def __init__(self, query_type, clas, ttl=None, name=None, data=None,
                 internal_type=None):
        self.type = query_type
        self.clas = clas  # Always IN
        self.ttl = ttl  # in seconds
        self.name = name  # CNAME
        self.data = data  # A, NS or something, depending at type
        self.internal_type = internal_type

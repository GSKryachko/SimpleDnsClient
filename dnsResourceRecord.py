from PackageTypeEnums import package_type


class DnsResourceRecord:
    def __init__(self, type, clas, ttl, address):
        self.type = type
        self.clas = clas
        self.ttl = ttl
        self.address = address

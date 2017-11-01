from PackageTypeEnums import package_type


class DnsResourceRecord:
    def __init__(self, type, clas, ttl, address, internal_type):
        self.type = type
        self.clas = clas
        self.ttl = ttl
        self.address = address
        self.internal_type = internal_type

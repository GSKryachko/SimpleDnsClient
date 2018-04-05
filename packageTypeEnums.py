from enum import Enum


class PackageType(Enum):
    AAAA = b'\x00\x1c'
    CNAME = b'\x00\x05'
    A = b'\x00\x01'
    NS = b'\x00\x02'
    SOA = b'\x00\x06'
    
    @staticmethod
    def parse(string):
        try:
            return PackageType[string.upper()]
        except KeyError:
            print(string + ' is not supported package type')

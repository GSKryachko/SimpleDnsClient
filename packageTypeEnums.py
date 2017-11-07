from enum import Enum


class PackageType(Enum):
    AAAA = b'\x00\x1c'
    CNAME = b'\x00\x05'
    A = b'\x00\x01'
    NS = b'\x00\x02'
    
    @staticmethod
    def parse(string):
        if string == 'AAAA':
            return PackageType.AAAA
        if string == 'A':
            return PackageType.A
        if string == 'NS':
            return PackageType.NS
        if string == 'CNAME':
            return PackageType.CNAME
        raise ValueError(string + ' is not supported package type')

from enum import Enum


class package_type(Enum):
    AAAA = b'\x00\x1c'
    CNAME = b'\x00\x05'
    A = b'\x00\x01'
    NS = b'\x00\x02'

    @staticmethod
    def parse(string):
        if string == 'AAAA':
            return package_type.AAAA
        if string == 'A':
            return package_type.A
        if string == 'NS':
            return package_type.NS
        if string == 'CNAME':
            return package_type.CNAME
        raise ValueError(string + ' is not supported package type')
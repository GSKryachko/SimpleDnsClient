from enum import Enum
class package_type(Enum):
    AAAA = b'\x00\x1c'
    CNAME = b'\x00\x05'
    A = b'\x00\x01'
    NS = b'\x00\x02'
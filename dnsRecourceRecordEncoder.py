# @staticmethod
import struct

from packageTypeEnums import PackageType


def encode_resource_record(record):
    encoded = []
    encoded.append(encode_address_with_hex_prefixes(record.name))
    encoded.append(record.type.value)
    if record.clas != 'IN':
        raise ValueError('Only IN class requests are supported')
    encoded.append(((1).to_bytes(2, 'big')))
    encoded.append(struct.pack('>I', record.ttl))
    data = encode_data(record.data, record.type)
    encoded.append(struct.pack('>H', len(data)))
    encoded.append(data)
    return b''.join(encoded)


# @staticmethod
def encode_address_with_hex_prefixes(address):
    ans = b''
    for word in address.split('.'):
        ans += bytes([len(word)]) + word.encode('ASCII')
    ans += b'\x00'
    return ans


def encode_data(data, record_type):
    if record_type == PackageType.CNAME:
        return encode_address_with_hex_prefixes(data)
    raise ValueError("Unsupported record type {}".format(record_type.value))

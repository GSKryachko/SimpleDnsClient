import struct

import os

from packageTypeEnums import PackageType

def parse_resource_record(record):
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


def decode_canonical_name(byte_stream):
    chunk_size_byte = byte_stream.read(1)
    chunk_size = ord(chunk_size_byte)
    address = []
    while chunk_size > 0:
        if chunk_size >= 192:
            raise ValueError('Message compression is not supported')
        chunk = byte_stream.read(chunk_size).decode()
        address.append(chunk)
        chunk_size = ord(byte_stream.read(1))
    
    return '.'.join(address)

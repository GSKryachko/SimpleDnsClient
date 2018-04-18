import struct

from packageTypeEnums import PackageType

__all__ = ['encode_package']


def encode_package(dns_package):
    dns = b''
    dns += dns_package.transaction_id
    flag = 0
    flag |= int(dns_package.recursive)
    flag *= 2 ** 8
    dns += flag.to_bytes(2, 'big')
    dns += len(dns_package.questions).to_bytes(2, 'big')
    dns += len(dns_package.answers).to_bytes(2, 'big')
    dns += len(dns_package.authority_records).to_bytes(2, 'big')
    dns += len(dns_package.additional_records).to_bytes(2, 'big')
    
    for question in dns_package.questions:
        dns += encode_question(question)
    for record in dns_package.answers:
        dns += encode_resource_record(record)
    for record in dns_package.authority_records:
        dns += encode_resource_record(record)
    for record in dns_package.additional_records:
        dns += encode_resource_record(record)
    return dns


def encode_question(question):
    ans = []
    ans.append(encode_address_with_hex_prefixes(question.name))
    ans.append(question.type.value)
    ans.append((1).to_bytes(2, 'big'))
    return b''.join(ans)


def encode_address_with_hex_prefixes(address):
    ans = b''
    for word in address.split('.'):
        ans += bytes([len(word)]) + word.encode('ASCII')
    ans += b'\x00'
    return ans

def encode_ip(ip):
    return bytes([int(x) for x in ip.split('.')])

def encode_resource_record(record):
    encoded = []
    encoded.append(
        encode_address_with_hex_prefixes(record.name))
    encoded.append(record.type.value)
    if record.clas != b'\x00\x01':
        raise ValueError('Only IN class requests are supported')
    encoded.append(((1).to_bytes(2, 'big')))
    encoded.append(struct.pack('>I', record.ttl))
    data = encode_data(record.data, record.type)
    encoded.append(struct.pack('>H', len(data)))
    encoded.append(data)
    return b''.join(encoded)


def encode_data(data, record_type):
    if record_type in [PackageType.CNAME, PackageType.NS]:
        return encode_address_with_hex_prefixes(data)
    if record_type == PackageType.A:
        return encode_ip(data)
    raise ValueError(
        "Unsupported record type {}".format(record_type.value))

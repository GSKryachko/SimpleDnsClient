import struct

from domain.dnsHeader import DnsHeader
from domain.dnsPackage import DnsPackage
from packageTypeEnums import PackageType

__all__ = ['encode_package']


def encode_package(dns_package: DnsPackage):
    encoded = [encode_header(dns_package.header)]
    encoded.extend([encode_question(x) for x in dns_package.questions])
    encoded.extend([encode_resource_record(x) for x in dns_package.answers])
    encoded.extend([encode_question(x) for x in dns_package.authority_records])
    encoded.extend(
        [encode_question(x) for x in dns_package.additional_records])
    return b''.join(encoded)


def encode_header(header: DnsHeader):
    ans = [header.transaction_id, header.flags,
           header.questions_count.to_bytes(2, 'big'),
           header.answers_count.to_bytes(2, 'big'),
           header.authority_count.to_bytes(2, 'big'),
           header.additional_count.to_bytes(2, 'big')]
    return b''.join(ans)


def encode_question(question):
    ans = [encode_address_with_hex_prefixes(question.name),
           question.type.value, (1).to_bytes(2, 'big')]
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
    encoded = [encode_address_with_hex_prefixes(record.name),
               record.type.value]
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

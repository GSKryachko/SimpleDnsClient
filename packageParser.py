import io
import os
from struct import *

from domain.dnsHeader import DnsHeader
from domain.dnsPackage import DnsPackage
from domain.dnsResourceRecord import DnsResourceRecord
from packageTypeEnums import PackageType

__all__ = ['parse_response']


def decode_canonical_name(byte_stream):
    chunk_size_byte = byte_stream.read(1)
    chunk_size = ord(chunk_size_byte)
    address = []
    while chunk_size > 0:
        if chunk_size >= 192:
            byte_stream.seek(-1, os.SEEK_CUR)
            offset = decode_offset(byte_stream.read(2))
            pos = byte_stream.tell()
            byte_stream.seek(offset, os.SEEK_SET)
            address.append(decode_canonical_name(byte_stream))
            byte_stream.seek(pos, os.SEEK_SET)
            break
        chunk = byte_stream.read(chunk_size).decode()
        address.append(chunk)
        chunk_size = ord(byte_stream.read(1))
    
    return '.'.join(address)


def decode_offset(offset):
    offset = bytearray(offset)
    for i in range(len(offset)):
        offset[i] &= b'\x3f\xff'[i]
    offset = unpack('>h', offset)[0]
    return offset


def decode_AAAA_address(byte_stream):
    adr = []
    for i in range(8):
        adr.append(
            '{:02x}'.format(ord(byte_stream.read(1))) + '{:02x}'.format(
                ord(byte_stream.read(1))))
    return ':'.join(adr)


def decode_id(byte_stream):
    return '.'.join(str(quartet) for quartet in byte_stream.read(4))


def parse_question(byte_stream, internal_type='question'):
    address = decode_canonical_name(byte_stream)
    type = PackageType(byte_stream.read(2))
    clas = byte_stream.read(2)
    return DnsResourceRecord(type, clas, name=address,
                             internal_type=internal_type)


def parse_answer(byte_stream, internal_type):
    name = decode_canonical_name(byte_stream)
    ans_type = PackageType(byte_stream.read(2))
    clas = byte_stream.read(2)
    ttl = unpack('>I', byte_stream.read(4))[0]
    data_length = unpack('>h', byte_stream.read(2))[0]
    # try:
    address = decode_address(byte_stream, ans_type)
    # except ValueError:
    #     return
    return DnsResourceRecord(ans_type, clas, ttl, name=name, data=address,
                             internal_type=internal_type)


def decode_address(byte_stream, ans_type):
    if ans_type == PackageType.AAAA:
        return decode_AAAA_address(byte_stream)
    elif ans_type in [PackageType.NS, PackageType.CNAME, PackageType.SOA]:
        return decode_canonical_name(byte_stream)
    elif ans_type == PackageType.A:
        return decode_id(byte_stream)
    raise ValueError("Unsupported package type: ", ans_type)


def parse_header(byte_stream):
    transaction_id = byte_stream.read(2)
    flags = byte_stream.read(2)  # flags
    questions_count = unpack('>h', byte_stream.read(2))[0]
    answers_count = unpack('>h', byte_stream.read(2))[0]
    authority_count = unpack('>h', byte_stream.read(2))[0]
    additional_count = unpack('>h', byte_stream.read(2))[0]
    return DnsHeader(transaction_id, flags, questions_count, answers_count,
                     authority_count, additional_count)


def parse_response(resp):
    resp = io.BytesIO(resp)
    header = parse_header(resp)
    questions = [parse_question(resp) for x in
                 range(header.questions_count)]
    answers = [parse_answer(resp, 'answer') for x in
               range(header.answers_count)]
    authority = [parse_answer(resp, 'authority') for x in
                 range(header.authority_count)]
    additional = [parse_answer(resp, 'additional') for x in
                  range(header.additional_count)]
    return DnsPackage(header, questions, answers, authority, additional)

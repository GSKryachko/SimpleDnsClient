from struct import *
import io

import os

from dnsResourceRecord import DnsResourceRecord
from packageTypeEnums import PackageType


class ResponseHandler:
    transaction_id = b''
    questions_count = 0
    answer_count = 0
    authority_count = 0
    additional_count = 0
    questions = []
    answers = []
    authority = []
    additional = []
    
    def decode_canonical_name(self, byte_stream):
        chunk_size_byte = byte_stream.read(1)
        chunk_size = ord(chunk_size_byte)
        address = []
        while chunk_size > 0:
            if chunk_size >= 192:
                byte_stream.seek(-1, os.SEEK_CUR)
                offset = self.decode_offset(byte_stream.read(2))
                pos = byte_stream.tell()
                byte_stream.seek(offset, os.SEEK_SET)
                address.append(self.decode_canonical_name(byte_stream))
                byte_stream.seek(pos, os.SEEK_SET)
                break
            chunk = byte_stream.read(chunk_size).decode()
            address.append(chunk)
            chunk_size = ord(byte_stream.read(1))
        
        return '.'.join(address)
    
    def decode_offset(self, offset):
        offset = bytearray(offset)
        for i in range(len(offset)):
            offset[i] &= b'\x3f\xff'[i]
        offset = unpack('>h', offset)[0]
        return offset
    
    def decode_AAAA_address(self, byte_stream):
        adr = []
        for i in range(8):
            adr.append('{:02x}'.format(ord(byte_stream.read(1))) + '{:02x}'.format(ord(byte_stream.read(1))))
        return ':'.join(adr)
    
    def decode_id(self, byte_stream):
        return '.'.join(str(quartet) for quartet in byte_stream.read(4))
    
    def parse_question(self, byte_stream,internal_type = 'question'):
        address = self.decode_canonical_name(byte_stream)
        type = byte_stream.read(2)
        clas = byte_stream.read(2)
        self.questions.append(DnsResourceRecord(type, clas, address=address,internal_type=internal_type))
    
    def parse_answer(self, byte_stream, records_list, internal_type):
        name = self.decode_canonical_name(byte_stream)
        ans_type = byte_stream.read(2)
        clas = byte_stream.read(2)
        ttl = unpack('>I', byte_stream.read(4))[0]
        data_length = unpack('>h', byte_stream.read(2))[0]
        address = self.decode_address(byte_stream, ans_type)
        records_list.append(DnsResourceRecord(ans_type, clas, ttl, address, internal_type=internal_type))
    
    def decode_address(self, byte_stream, ans_type):
        if ans_type == PackageType.AAAA.value:
            return self.decode_AAAA_address(byte_stream)
        elif ans_type == PackageType.NS.value or ans_type == PackageType.CNAME.value:
            return self.decode_canonical_name(byte_stream)
        elif ans_type == PackageType.A.value:
            return self.decode_id(byte_stream)
        raise ValueError(ans_type + " package type is not supported")
    
    def parse_header(self, byte_stream):
        self.transaction_id = byte_stream.read(2)
        byte_stream.read(2)  # flags
        self.questions_count = unpack('>h', byte_stream.read(2))[0]
        self.answer_count = unpack('>h', byte_stream.read(2))[0]
        self.authority_count = unpack('>h', byte_stream.read(2))[0]
        self.additional_count = unpack('>h', byte_stream.read(2))[0]
    
    def clear_all_queries(self):
        self.answers.clear()
        self.questions.clear()
        self.authority.clear()
        self.additional.clear()
    
    def parse_response(self, resp):
        self.clear_all_queries()
        resp = io.BytesIO(resp)
        self.parse_header(resp)
        
        for i in range(self.questions_count):
            self.parse_question(resp)
        
        for i in range(self.answer_count):
            self.parse_answer(resp, self.answers, 'answer')
        
        for i in range(self.authority_count):
            self.parse_answer(resp, self.authority, 'authority')
        
        for i in range(self.additional_count):
            self.parse_answer(resp, self.additional, 'additional')

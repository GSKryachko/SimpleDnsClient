from struct import *
import io

import os

from PackageTypeEnums import package_type


class ResponseHandler:
    transaction_id = b''
    questions_count = 0
    answer_count = 0
    authority_count = 0
    additional_count = 0
    questions = []
    answer_common_part = ""
    last_answer = ""
    
    def decode_canonical_name(self, byte_stream):
        chunk_size = ord(byte_stream.read(1))
        chunk_number = 0
        address = []
        while chunk_size > 0:
            if chunk_size == 192:
                chunk = byte_stream.read(1).decode()
                if chunk == '+':
                    address += self.last_answer[chunk_number:]
                    break
                byte_stream.seek(-1,os.SEEK_CUR)
            chunk = byte_stream.read(chunk_size).decode()
            
            chunk_number += 1
            address.append(chunk)
            chunk_size = ord(byte_stream.read(1))

        self.last_answer = address
        return '.'.join(address)
   
    
    def decode_first_chunk_of_canonical_name(self, byte_stream):
        chunk_size = ord(byte_stream.read(1))
        return byte_stream.read(chunk_size).decode() + '.'
    
    def decode_AAAA_address(self, byte_stream):
        adr = ""
        for i in range(8):
            adr += '{:02x}'.format(ord(byte_stream.read(1))) + '{:02x}'.format(ord(byte_stream.read(1))) + ':'
        return adr
    
    def decode_id(self, byte_stream):
        return '.'.join(str(quartet) for quartet in byte_stream.read(4))
    
    def parse_answer(self, byte_stream):
        byte_stream.read(2)
        ans_type = byte_stream.read(2)
        # print('type', ans_type)
        clas = byte_stream.read(2)
        # print('class', clas)
        ttl = unpack('>I', byte_stream.read(4))[0]
        # print(ttl)
        data_length = unpack('>h', byte_stream.read(2))[0]
        if ans_type == package_type.AAAA.value:
            address = self.decode_AAAA_address(byte_stream)
        elif ans_type == package_type.A.value or ans_type == package_type.NS.value:
            address = self.decode_canonical_name(byte_stream)
        elif data_length == 4:
            address = self.decode_id(byte_stream)
        elif data_length == 16:
            address = self.decode_canonical_name(byte_stream)
        
        print(address)
    
    def parse_response(self, resp):
        resp = io.BytesIO(resp)
        self.transaction_id = resp.read(2)
        resp.read(2)  # flags
        self.questions_count = unpack('>h', resp.read(2))[0]
        self.answer_count = unpack('>h', resp.read(2))[0]
        self.authority_count = unpack('>h', resp.read(2))[0]
        self.additional_count = unpack('>h', resp.read(2))[0]
        
        print(self.transaction_id)
        print(self.questions_count)
        print(self.answer_count)
        print(self.authority_count)
        print(self.additional_count)
        
        for i in range(self.questions_count):
            address = self.decode_canonical_name(resp)
            self.answer_common_part = None
            type = resp.read(2)
            clas = resp.read(2)
            print(address)
            # print(type)
            # print(clas)
            #
        for i in range(self.answer_count):
            self.parse_answer(resp)
        
        for i in range(self.authority_count):
            self.parse_answer(resp)
        
        for i in range(self.additional_count):
            self.parse_answer(resp)

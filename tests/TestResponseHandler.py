import io
import unittest
from packageParser import PackageParser


class TestResponseHandler(unittest.TestCase):
    def setUp(self):
        self.response_handler = PackageParser()
    
    def test_decode_CNAME(self):
        address_in_bytes = io.BytesIO(b'\x03www\x09microsoft\x03com\x00')
        expected_decoded_address = 'www.microsoft.com'
        actual_decoded_address = self.response_handler.decode_canonical_name(address_in_bytes)
        self.assertEqual(expected_decoded_address, actual_decoded_address)
    
    def test_decode_canonical_name_from_one_chunk(self):
        address_in_bytes = io.BytesIO(b'\x03com\x00')
        expected_decoded_address = 'com'
        actual_decoded_address = self.response_handler.decode_canonical_name(address_in_bytes)
        self.assertEqual(expected_decoded_address, actual_decoded_address)
    
    def test_decode_A(self):
        id_in_bytes = io.BytesIO(b'\xca\x0c\x1b\x21')
        expected_decoded_addres = '202.12.27.33'
        actual_decoded_address = self.response_handler.decode_id(id_in_bytes)
        self.assertEqual(expected_decoded_addres, actual_decoded_address)
    
    def test_decode_offset(self):
        offset_in_bytes = b'\xc0\x5a'
        expected_offset = 90
        actual_offset = self.response_handler.decode_offset(offset_in_bytes)
        self.assertEqual(expected_offset, actual_offset)
    
    def test_decode_AAAA(self):
        address_in_bytes = io.BytesIO(b'\xca\x0c\x1b\x21\xca\x0c\x1b\x21\xca\x0c\x1b\x21\xca\x0c\x1b\x21')
        expected_decoded_address = 'ca0c:1b21:ca0c:1b21:ca0c:1b21:ca0c:1b21'
        actual_decoded_address = self.response_handler.decode_AAAA_address(address_in_bytes)
        self.assertEqual(expected_decoded_address, actual_decoded_address)
    
    def test_parse_question(self):
        self.response_handler.clear_all_queries()

        question_in_bytes = io.BytesIO(b'\x03com\x00\x00\x02\x00\x01')
        self.response_handler.parse_question(question_in_bytes)
        answer = self.response_handler.questions[0]
        self.assertEqual('com', answer.address)
        self.assertEqual(b'\x00\x02', answer.type)
        self.assertEqual(b'\x00\x01', answer.clas)
    
    def test_parse_answer(self):
        self.response_handler.clear_all_queries()

        answer_in_bytes = io.BytesIO(b'\x03com\x00\x00\x01\x00\x01\x00\x00\x01\x2c\x00\x04\xd4\xc1\xa3\x07')
        self.response_handler.parse_answer(answer_in_bytes, self.response_handler.answers)
        answer = self.response_handler.answers[0]
        self.assertEqual(b'\x00\x01', answer.type)
        self.assertEqual(b'\x00\x01', answer.clas)
        self.assertEqual(300, answer.ttl)
        self.assertEqual('212.193.163.7', answer.address)

    def test_decode_CNAME_with_offset(self):
        address_in_bytes = io.BytesIO(b'\x03www\xc0\x0c\x04fail\x00\x04pass\x00')
        expected_cname = 'www.pass'
        actual_cname = self.response_handler.decode_canonical_name(address_in_bytes)
        self.assertEqual(expected_cname,actual_cname)
    
    def test_parse_header(self):
        header_in_bytes = io.BytesIO(b'\x0d\x25\x85\x00\x00\x01\x00\x02\x00\x04\x00\x08')
        self.response_handler.parse_header(header_in_bytes)
        self.assertEqual(b'\x0d\x25', self.response_handler.transaction_id)
        self.assertEqual(1, self.response_handler.questions_count)
        self.assertEqual(2, self.response_handler.answer_count)
        self.assertEqual(4, self.response_handler.authority_count)
        self.assertEqual(8, self.response_handler.additional_count)

    def test_clear_all_queries(self):
        self.response_handler.answers.append(None)
        self.response_handler.questions.append(None)
        self.response_handler.authority.append(None)
        self.response_handler.additional.append(None)
        
        self.response_handler.clear_all_queries()

        self.assertEqual(self.response_handler.answers,[])
        self.assertEqual(self.response_handler.questions, [])
        self.assertEqual(self.response_handler.authority, [])
        self.assertEqual(self.response_handler.additional, [])
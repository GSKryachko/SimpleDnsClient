import io
import unittest
import RequestHandler
from ResponseHandler import ResponseHandler


class TestRequestHandler(unittest.TestCase):
    def test_address_encoding(self):
        address = 'www.microsoft.com'
        expected_encoded_address = b'\x03www\x09microsoft\x03com\x00'
        actual_encoded_address = RequestHandler.encode_address_with_hex_prefixes(address)
        self.assertEqual(expected_encoded_address, actual_encoded_address)
    
    def test_first_chunk_decoder(self):
        address_in_bytes = io.BytesIO(b'\x03www\x09microsoft\x03com\x00')
        
        expected_decoded_address = 'www.'
        response_handler = ResponseHandler()
        actual_decoded_address = response_handler.decode_first_chunk_of_canonical_name(address_in_bytes)
        self.assertEqual(expected_decoded_address, actual_decoded_address)

    def test_canonical_name_decoder(self):
        address_in_bytes = io.BytesIO(b'\x03www\x09microsoft\x03com\x00')
        expected_decoded_address = 'www.microsoft.com.'
        response_handler = ResponseHandler()
        actual_decoded_address = response_handler.decode_canonical_name(address_in_bytes)
        self.assertEqual(expected_decoded_address, actual_decoded_address)
    
    def test_canonical_name_decoder_with_common_name(self):
        first_address = io.BytesIO(b'\x03ns1\x06google\x03com\x00')
        second_address = io.BytesIO(b'\x03ns2\x06google\x03com\x00')
        response_handler = ResponseHandler()
        response_handler.decode_canonical_name(first_address)
        self.assertEqual(response_handler.answer_common_part, 'google.com.')
        second_address_decoded = response_handler.decode_canonical_name(second_address)
        self.assertEqual(second_address_decoded,'ns2.google.com.')
        
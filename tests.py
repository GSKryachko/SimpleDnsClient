import io
import unittest
import RequestHandler
from ResponseHandler import ResponseHandler


class TestRequestHandler(unittest.TestCase):
    def test_address_encoding(self):
        address = 'www.microsoft.com'
        expected_encoded_address = b'\x03www\x09microsoft\x03com\x00'
        actual_encoded_address = RequestHandler.RequestHandler('UDP').encode_address_with_hex_prefixes(address)
        self.assertEqual(expected_encoded_address, actual_encoded_address)
    
    def test_first_chunk_decoder(self):
        address_in_bytes = io.BytesIO(b'\x03www\x09microsoft\x03com\x00')
        expected_decoded_address = 'www.'
        response_handler = ResponseHandler()
        actual_decoded_address = response_handler.decode_first_chunk_of_canonical_name(address_in_bytes)
        self.assertEqual(expected_decoded_address, actual_decoded_address)
    
    def test_canonical_name_decoder(self):
        address_in_bytes = io.BytesIO(b'\x03www\x09microsoft\x03com\x00')
        expected_decoded_address = 'www.microsoft.com'
        response_handler = ResponseHandler()
        actual_decoded_address = response_handler.decode_canonical_name(address_in_bytes)
        self.assertEqual(expected_decoded_address, actual_decoded_address)
    
    def test_decode_canonical_name_from_one_chunk(self):
        address_in_bytes = io.BytesIO(b'\x03com\x00')
        expected_decoded_address = 'com'
        response_handler = ResponseHandler()
        actual_decoded_address = response_handler.decode_canonical_name(address_in_bytes)
        self.assertEqual(expected_decoded_address, actual_decoded_address)


    def test_decode_id(self):
        pass
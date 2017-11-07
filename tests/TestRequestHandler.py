import io
import unittest
import requestHandler


class TestRequestHandler(unittest.TestCase):
    def test_encode_address(self):
        address = 'www.microsoft.com'
        expected_encoded_address = b'\x03www\x09microsoft\x03com\x00'
        actual_encoded_address = requestHandler.RequestHandler().encode_address_with_hex_prefixes(address)
        self.assertEqual(expected_encoded_address, actual_encoded_address)
    
    def test_create_request(self):
        req_handler = requestHandler.RequestHandler()
        expected_request = b'\xAB\xCD\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03com\x00\x00\x01\x00\x01'
        actual_request = req_handler.create_request('com',recursive=False)
        self.assertEqual(expected_request,actual_request)


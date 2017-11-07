import io
import unittest
import requestHandler


class TestRequestHandler(unittest.TestCase):
    def test_address_encoding(self):
        address = 'www.microsoft.com'
        expected_encoded_address = b'\x03www\x09microsoft\x03com\x00'
        actual_encoded_address = requestHandler.RequestHandler('UDP').encode_address_with_hex_prefixes(address)
        self.assertEqual(expected_encoded_address, actual_encoded_address)
    



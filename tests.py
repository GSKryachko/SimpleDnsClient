import unittest
import RequestHandler

class RequestHandlerTest(unittest.TestCase):
    def test_address_encoding(self):
        address = 'www.microsoft.com'
        expected_encoded_address = b'\x03www\x09microsoft\x03com\x00'
        actual_encoded_address = RequestHandler.encode_address_with_hex_prefixes(address)
        self.assertEquals(expected_encoded_address,actual_encoded_address)
       #
        #  expected_encoded = b'\0x09' + microsoft.encode('ASCII') +0x03 bytes('com') 0x00

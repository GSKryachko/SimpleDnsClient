import unittest
import dnsRecourceRecordEncoder


class TestResourceRecordEncoder(unittest.TestCase):
    def test_encode_address(self):
        address = 'www.microsoft.com'
        expected_encoded_address = b'\x03www\x09microsoft\x03com\x00'
        actual_encoded_address = dnsRecourceRecordEncoder.encode_address_with_hex_prefixes(address)
        self.assertEqual(expected_encoded_address, actual_encoded_address)

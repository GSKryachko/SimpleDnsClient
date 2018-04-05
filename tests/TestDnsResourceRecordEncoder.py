import unittest

from dnsRecourceRecordEncoder import *
from dnsResourceRecord import DnsResourceRecord
from packageTypeEnums import *


class TestRequestHandler(unittest.TestCase):
    def test_parse_package_type(self):
        expected = b'\x07clients\x01l\x06google\x03com\x00\x00\x05\x00\x01\x00\x00\x00\x99\x00\x16\x07clients\x01l\x06google\x03com\x00'
        record = DnsResourceRecord(PackageType.CNAME, clas='IN', ttl=153,
                                   name='clients.l.google.com',
                                   data='clients.l.google.com')
        actual = encode_resource_record(record)
        self.assertEqual(actual, expected)

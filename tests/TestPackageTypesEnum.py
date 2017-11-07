import unittest
from packageTypeEnums import PackageType


class TestRequestHandler(unittest.TestCase):
    def test_parse_package_type(self):
        self.assertEqual(PackageType.A, PackageType.parse('A'))
        self.assertEqual(PackageType.AAAA, PackageType.parse('AAAA'))
        self.assertEqual(PackageType.NS, PackageType.parse('NS'))
        self.assertEqual(PackageType.CNAME, PackageType.parse('CNAME'))

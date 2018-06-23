import unittest

from domain.dnsResourceRecord import DnsResourceRecord
from packageTypeEnums import PackageType
from serverCash import Cash


class TestServerCash(unittest.TestCase):
    def test_registration(self):
        cash = Cash()
        record = DnsResourceRecord(PackageType.CNAME, clas='IN', ttl=153,
                                   name='clients.l.google.com',
                                   data='clients.l.google.com')
        cash.register_entry(record)
        self.assertEqual(cash.get_answer(record),record)
    
    def test_saving(self):
        cash = Cash()
        cash.register_entry(('test.com', '1.2.3.4'))
        cash.save(file='test_cash.json')
        cash.name_to_data.clear()
        cash.data_to_name.clear()
        
        cash.load(file='test_cash.json')
        self.assertEqual(cash.data_to_name['1.2.3.4'], 'test.com')
        self.assertEqual(cash.name_to_data['test.com'], '1.2.3.4')

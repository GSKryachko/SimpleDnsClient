import unittest

from serverCash import Cash


class TestServerCash(unittest.TestCase):
    def test_registration(self):
        cash = Cash()
        cash.register_entry(('test.com', '1.2.3.4'))
        self.assertEqual(cash.ip_to_name['1.2.3.4'], 'test.com')
        self.assertEqual(cash.name_to_ip['test.com'], '1.2.3.4')
    
    def test_saving(self):
        cash = Cash()
        cash.register_entry(('test.com', '1.2.3.4'))
        cash.save(file='test_cash.json')
        cash.name_to_ip.clear()
        cash.ip_to_name.clear()
        
        cash.load(file='test_cash.json')
        self.assertEqual(cash.ip_to_name['1.2.3.4'], 'test.com')
        self.assertEqual(cash.name_to_ip['test.com'], '1.2.3.4')

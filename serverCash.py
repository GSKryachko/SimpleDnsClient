import pickle
import time
from collections import defaultdict

from domain.dnsResourceRecord import DnsResourceRecord


class Cash:
    def __init__(self):
        self.cash = defaultdict(defaultdict)
    
    def get_answer(self, record: DnsResourceRecord):
        print('requesting name {} of type {}'.format(record.name, record.type))
        if record.type in self.cash:
            return self.cash[record.type].get(record.name)
        return None
    
    def register_entry(self, record: DnsResourceRecord):
        record.registration_time = time.time()
        self.cash[record.type][record.name] = record
    
    def refresh_cash(self):
        for record_type in self.cash.keys():
            for record in list(self.cash[record_type].values()):
                if record.registration_time + record.ttl < time.time():
                    self.cash[record_type].pop(record.name)
                    print('removing', record.name)
    
    def save(self, file='server_cash.pickle'):
        with open(file, 'wb') as f:
            f.write(pickle.dumps(self.cash))
    
    def load(self, file='server_cash.pickle'):
        try:
            with open(file, 'rb') as f:
                self.cash = pickle.load(f)
        except FileNotFoundError:
            pass
    
    def register_package(self, package):
        print("registering package...")
        for record in package.answers:
            self.register_entry(record)
        for record in package.authority_records:
            self.register_entry(record)
        for record in package.additional_records:
            self.register_entry(record)
    
    def assure_consistency(self):
        while True:
            self.refresh_cash()
            time.sleep(60)
    
    def print(self):
        for record_type in self.cash.values():
            for record in record_type.values():
                print(record.name, record.type)

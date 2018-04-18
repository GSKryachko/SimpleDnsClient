import pickle
import time

from packageTypeEnums import PackageType


class Cash:
    def __init__(self):
        self.a = {}
        self.ns = {}
    
    def get_answer(self, record):
        if record.type == PackageType.A:
            return self.a.get(record.name, None)
        if record.type == PackageType.NS:
            return self.ns.get(record.name, None)
        return None
    
    def register_entry(self, record):
        if record.type not in [PackageType.A, PackageType.NS,
                               PackageType.CNAME]:
            return
        if record.type == PackageType.A:
            self.a[record.name] = record
        if record.type == PackageType.NS:
            self.ns[record.name] = record
    
    def refresh_cash(self):
        for record in list(self.a.values()):
            if record.ttl < time.time():
                self.a.pop(record.name)
                self.ns.pop(record.data)
    
    def save(self, file='server_cash.pickle'):
        with open(file, 'wb') as f:
            f.write(pickle.dumps([self.a, self.ns]))
    
    def load(self, file='server_cash.pickle'):
        try:
            with open(file, 'rb') as f:
                self.a, self.ns = pickle.load(f)
        except FileNotFoundError:
            pass
    
    def register_package(self, package):
        for record in package.answers:
            self.register_entry(record)
        for record in package.authority_records:
            self.register_entry(record)
        for record in package.additional_records:
            self.register_entry(record)
    
    def assure_consistency(self):
        while True:
            # self.refresh_cash()
            time.sleep(60)

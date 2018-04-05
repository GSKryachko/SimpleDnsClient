import json


class Cash:
    def __init__(self):
        self.name_to_ip = {}
        self.ip_to_name = {}
    
    def register_entry(self, entry):
        """Accepts entry as tuple (name, ip)"""
        self.name_to_ip[entry[0]] = entry[1]
        self.ip_to_name[entry[1]] = entry[0]
    
    def refresh_cash(self):
        pass
    
    def save(self, file='server_cash.json'):
        with open(file, 'w') as f:
            f.write(json.dumps([self.name_to_ip, self.ip_to_name]))
    
    def load(self, file='server_cash.json'):
        with open(file, 'r') as f:
            self.name_to_ip, self.ip_to_name = json.loads(f.read())

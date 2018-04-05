class DnsPackage:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.authority_records = []
        self.additional_records = []
        self.request_type = []
class DnsPackage:
    def __init__(self, header, questions, answers,
                 authority_records, additional_records):
        self.header = header
        self.questions = questions
        self.answers = answers
        self.authority_records = authority_records
        self.additional_records = additional_records

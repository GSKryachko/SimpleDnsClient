class DnsPackage:
    def __init__(self, transaction_id, questions, answers,
                 authority_records, additional_records, recursive=True):
        self.transaction_id = transaction_id
        self.recursive = recursive
        self.questions = questions
        self.answers = answers
        self.authority_records = authority_records
        self.additional_records = additional_records

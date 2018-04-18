class DnsHeader:
    def __init__(self, transaction_id, flags, questions_count, answers_count,
                 authority_records_count, additional_records_count):
        self.transaction_id = transaction_id
        self.flags = flags
        self.questions_count = questions_count
        self.answers_count = answers_count
        self.authority_count = authority_records_count
        self.additional_count = additional_records_count

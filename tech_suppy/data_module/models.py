class MessageInfo:
    def __init__(self, id, user_id, query, date):
        self.id = id
        self.user_id = user_id
        self.query = query
        self.date = date


class MailingMessage:
    def __init__(self, id, user_id, query, operator_answer):
        self.id = id
        self.user_id = user_id
        self.query = query
        self.operator_answer = operator_answer


class ChatInfo:
    def __init__(self, user_id, query, date, answered, answer=None, source=None, operator_answered=False):
        self.user_id = user_id
        self.query = query
        self.date = date
        self.answer = answer
        self.source = source
        self.operator_answered = operator_answered
        self.answered = answered


class Operator:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password



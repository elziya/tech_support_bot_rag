from data_module import get_mailing_messages as _get_mailing_messages, update_mailing_message_by_id \
    as _update_mailing_message_by_id


def get_mailing_messages():
    return _get_mailing_messages()


def update_mailing_message_by_id(id):
    _update_mailing_message_by_id(id)
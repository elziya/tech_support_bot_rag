from data_module import get_unanswered_messages as _get_unanswered_messages, get_message_by_id as _get_message_by_id, \
    update_chat_info_by_id as _update_chat_info_by_id, get_operator_by_username, save_sources, SourceType
from documentation_module import upload_documentation as _upload_documentation


def get_unanswered_messages(operator_id):
    return _get_unanswered_messages(operator_id)


def get_message_by_id(message_id, operator_id):
    return _get_message_by_id(message_id, operator_id)


def update_chat_info_by_id(id, answer):
    _update_chat_info_by_id(id, answer)


def upload_documentation(docs):
    save_sources(docs, SourceType.HTML)
    _upload_documentation(docs)


def sign_in(username, password, bcrypt):
    operator = get_operator_by_username(username)
    if operator and bcrypt.check_password_hash(operator.password, password):
        return True, operator.id
    return False, None

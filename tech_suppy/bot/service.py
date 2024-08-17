from data_module import save_chat_info as _save_chat_info, get_operator_for_query, get_source_id_by_name


def save_chat_info(chat_info):
    operator_id = get_operator_for_query()
    chat_info.source = get_source_id_by_name(chat_info.source)
    _save_chat_info(chat_info, operator_id)

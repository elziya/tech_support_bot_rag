from aiogram import types
from aiogram.filters import CommandObject
from rag_module import is_about_docs, get_answer
from data_module import ChatInfo
from bot.service import save_chat_info


async def ask(message: types.Message, command: CommandObject, rag_chain, vector_db, emb_model):
    if not command.args:

        return await message.answer(
            'Для того, чтобы узнать ответ на интересующий Вас вопрос, используйте /ask <вопрос>')
    else:
        query = command.args
        if not is_about_docs(query, vector_db, emb_model):
            save_chat_info(ChatInfo(message.chat.id, query, message.date, False))

            return await message.answer('Извините, не могу ответить на этот вопрос. Не в рамках моих знаний.\n'
                                        'Перенаправим этот вопрос оператору технической поддрежки!')
        else:
            await message.answer('Формирую ответ на Ваш вопрос...')

            response_text, source, is_hallucination = get_answer(query, rag_chain, emb_model)

            save_chat_info(ChatInfo(message.chat.id, query, message.date, not is_hallucination,
                                    answer=response_text, source=source))
            if is_hallucination:
                return await message.answer('Извините, не могу ответить на этот вопрос. Не в рамках моих знаний.\n'
                                            'Перенаправим этот вопрос оператору технической поддрежки!')

            return await message.answer(
                f'Отвечаю на вопрос:\n{command.args}\n\n{response_text}\n\nБольше можно посмотреть '
                f'здесь -> {source}')

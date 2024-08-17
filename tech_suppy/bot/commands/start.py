from aiogram import types


async def start(message: types.Message) -> None:
    await message.answer('Добрый день! Это бот технической поддержки Microsoft!\n'
                         'Отвечу Вам в любое время суток на вопросы, связанные с продуктами Microsoft, и обязательно '
                         'предоставлю источник, в котором Вы сможете прочитать больше!\n'
                         'Нажми команду /ask, чтобы задать вопрос!)')

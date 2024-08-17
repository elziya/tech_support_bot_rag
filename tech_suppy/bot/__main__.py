from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
import os
import asyncio
import logging
from bot.commands import register_user_commands, BOT_COMMANDS
from rag_module import get_chain, get_vector_db, get_model, get_tokenizer, get_embeddings_model, get_sent_transformer_model
from scheduler import on_startup


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in BOT_COMMANDS:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    await bot.set_my_commands(commands=commands_for_bot)
    register_user_commands(dp)

    embedding_model = get_embeddings_model()
    vector_db = get_vector_db(embedding_model)

    model = get_model()
    tokenizer = get_tokenizer()
    sent_transformer = get_sent_transformer_model()
    rag_chain = get_chain(vector_db, model, tokenizer)

    dp.startup.register(on_startup)
    await dp.start_polling(bot, vector_db=vector_db, rag_chain=rag_chain, emb_model=sent_transformer)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot is stopped')

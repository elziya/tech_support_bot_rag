import os

import aioschedule
import asyncio
from aiogram import Bot
from data_module import get_mailing_messages, update_mailing_message_by_id


async def send_operator_answers():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    messages = get_mailing_messages()
    for m in messages:
        await bot.send_message(m.user_id, f"Добрый день! Это оператор технической поддержки.\n"
                                       f"Вы задавали нам следующий вопрос: {m.query}\n\n"
                                       f"{m.operator_answer}")
        update_mailing_message_by_id(m.id)


async def scheduler():
    aioschedule.every(3).minutes.do(send_operator_answers)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup():
    asyncio.create_task(scheduler())
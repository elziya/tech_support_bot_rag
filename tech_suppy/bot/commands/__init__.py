__all__ = ['register_user_commands', 'BOT_COMMANDS']

from aiogram import Router
from aiogram.filters import CommandStart, Command

from bot.commands.start import start
from bot.commands.ask import ask


BOT_COMMANDS = (
    ("start", "начало работы с ботом"),
    ("ask", "задать вопрос")
)


def register_user_commands(router: Router) -> None:
    router.message.register(start, CommandStart())
    router.message.register(ask, Command(commands=['ask']))

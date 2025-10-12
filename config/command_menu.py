from aiogram import Bot
from aiogram.types import BotCommand

from config.app_settings import settings


async def set_command_menu(bot: Bot):
    command_menu = [
        BotCommand(command=command,
                   description=description
                   ) for command, description in settings.COMMAND_MENU.items()
    ]
    await bot.set_my_commands(command_menu)

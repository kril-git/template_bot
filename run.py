import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

# from routers.commands.base_commands import router
from routers import router as main_router
from sqlalchemy.ext.asyncio import async_sessionmaker
from models.base import engine
from utils.common import setup_logging, get_list_uuid_admins, set_command_menu
from utils.settings.app_settings import settings
from init import bot
from middleware.outer import OuterMiddlewareCommon

logger = logging.getLogger("my_app")


# bot = Bot(token=settings.BOT_TOKEN,
#           # parse_mode=ParseMode.HTML,
#           )


async def main():
    setup_logging()
    # bot = Bot(token=settings.BOT_TOKEN,
    #           # parse_mode=ParseMode.HTML,
    #           )
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.update.outer_middleware(OuterMiddlewareCommon())
    settings.ADMINS = await get_list_uuid_admins()
    settings.PATH_FOR_ALL_MEDIA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_media")
    # dp.startup.register(set_main_menu)
    await set_command_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

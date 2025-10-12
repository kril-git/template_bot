import asyncio
import logging
import os

from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from init import bot
from middleware.outer import OuterMiddlewareCommon
from models.base import engine
from routers import router as main_router
from services.services_admin import get_list_uuid_admins
from config.logger_config import setup_logging
from config.command_menu import set_command_menu
from config.app_settings import settings

logger = logging.getLogger("my_app")


async def main():
    setup_logging()
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

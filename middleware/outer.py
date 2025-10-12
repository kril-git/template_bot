import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db.crud import get_users_by_role, update_role_user_to_admin
from services.services_admin import update_role_to_admin

logger = logging.getLogger(__name__)


class OuterMiddlewareCommon(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        logger.info('Вошли в миддлварь %s, тип события %s',
                    __class__.__name__,
                    event.__class__.__name__)
        print("3333333333333333333333333333333")
        # for key, value in data.items():
        #     print(f"{key}: {value}")
        # await update_role_to_admin(user_id=2)
        # admin = await get_users_by_role()
        # print(admin)
        result = await handler(event, data)
        print(result)
        logger.debug('Выходим из миддлвари  %s', __class__.__name__)

        return result



import logging

from aiogram.types import InlineKeyboardMarkup

from db.crud import get_users_by_role
from services.bot_answer import bot_answer
from utils.ERoles import Roles

logger = logging.getLogger(__name__)


async def send_poll_from_json(chat_id: str | None,
                              text: str,
                              disable_notification: bool,
                              admin_uuid: str | None,
                              reply_markup: InlineKeyboardMarkup,
                              v: int
                              ) -> int:
    """
    chat_id: id пользователя, если None то передаем всем пользователям которые входят в группу USER
    text: Текст опроса
    disable_notification: не ясный параметр, по умолчанию False
    admin_uuid: id администратора который создал опрос, если None то не посылаем опрос администратору
    reply_markup: инлайн клавиатура с вопросами опроса
    """

    uuids_user: list[str] = []
    if chat_id is None:
        uuids_user = await get_users_by_role(role=Roles.USER)
    else:
        uuids_user.append(chat_id)

    if admin_uuid is not None:
        uuids_user.append(admin_uuid)

    count = await bot_answer(text=text,
                             disable_notification=disable_notification,
                             reply_markup=reply_markup,
                             users=uuids_user)
    return count



import asyncio
import logging

from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.exceptions import TelegramForbiddenError

from db.crud import get_users_by_role
from init import bot
from models import QuizOption
from utils.ERoles import Roles
from lexicon.message_constants.all_str_constants_ru import EMOJI_NUM

logger = logging.getLogger(__name__)


async def send_list_message(data: list, message: Message):

    for i in data:
        try:
            await message.answer(text=f"{i}\n", parse_mode=ParseMode.HTML)
        except TelegramRetryAfter as e:
            logger.error(f"Target: Flood limit is exceeded. "
                         f"Sleep {e.retry_after} seconds."
                         )
            await asyncio.sleep(e.retry_after)
        except TelegramForbiddenError:
            logger.info(f"Target [ID:{message.from_user.id}]: Bot Blocked")



async def send_message_text_to_user_handler(
        uuid: str,
        text: str,
        disable_notification: bool = False,
) -> bool:
    try:
        await bot.send_message(
            chat_id=uuid,
            text=text,
            disable_notification=disable_notification,
        )
    except TelegramRetryAfter as e:
        logger.error(f"Target [ID:{uuid}]: Flood limit is exceeded. "
                     f"Sleep {e.retry_after} seconds."
                     )
        await asyncio.sleep(e.retry_after)
        return await bot.send_message(
            chat_id=uuid,
            text=text,
            disable_notification=disable_notification,
        )
    except TelegramForbiddenError:
        logger.info(f"Target [ID:{uuid}]: Bot Blocked")
        # pass
    else:
        logger.info(f"Target [ID:{uuid}]: success")
        return True
    return False


async def send_video_to_user_handler(
        uuid: str,
        video: str,
        disable_notification: bool = False,
) -> bool:
    try:
        await bot.send_video(
            chat_id=uuid,
            video=video,
            disable_notification=disable_notification,
        )
    except TelegramRetryAfter as e:
        logger.error(f"Target [ID:{uuid}]: Flood limit is exceeded. "
                     f"Sleep {e.retry_after} seconds."
                     )
        await asyncio.sleep(e.retry_after)
        return await bot.send_video(
            chat_id=uuid,
            video=video,
            disable_notification=disable_notification,
        )
    except TelegramForbiddenError:
        logger.info(f"Target [ID:{uuid}]: Bot Blocked")
    else:
        logger.info(f"Target [ID:{uuid}]: success")
        return True
    return False


async def send_message_photo_to_user_handler(
        uuid: str,
        photo: str,
        caption: str | None,
        disable_notification: bool = False,
) -> bool:
    try:
        await bot.send_photo(
            chat_id=uuid,
            photo=photo,
            caption=caption,
            disable_notification=disable_notification,
        )
    except TelegramRetryAfter as e:
        logger.error(f"Target [ID:{uuid}]: Flood limit is exceeded. "
                     f"Sleep {e.retry_after} seconds."
                     )
        await asyncio.sleep(e.retry_after)
        return await bot.send_photo(
            chat_id=uuid,
            photo=photo,
            caption=caption,
            disable_notification=disable_notification,
        )
    except TelegramForbiddenError:
        logger.info(f"Target [ID:{uuid}]: Bot Blocked")
    else:
        logger.info(f"Target [ID:{uuid}]: success")
        return True
    return False


async def send_photo_and_text(data: dict, admin_uuid: str | None) -> int:
    uuids_user: list[str] = []
    count = 0

    if admin_uuid is not None:
        uuids_user.append(admin_uuid)
    else:
        uuids_user = await get_users_by_role(role=Roles.USER)
    try:
        for uuid in uuids_user:
            m1 = await send_message_text_to_user_handler(uuid=uuid, text=data.get("text"))
            m2 = await send_message_text_to_user_handler(uuid=uuid, text=data.get("mailing_text"))

            if data.get("photo") != "none":
                p1 = await send_message_photo_to_user_handler(uuid=uuid, photo=data.get("photo"), caption=None)
            else:
                p1 = True
            if m1 & m2 & p1:
                count += 1
            await asyncio.sleep(.05)
    finally:
        logger.info(f"{count} messages successful sent.")
        uuids_user.clear()
    return count


async def send_video_and_text(data: dict, admin_uuid: str | None, send_all_or_one: str | None) -> int:
    uuids_user: list[str] = []
    count = 0

    if admin_uuid is not None:
        uuids_user.append(admin_uuid)
    else:
        uuids_user = await get_users_by_role(role=Roles.USER)
    try:
        if send_all_or_one is None:
            for uuid in uuids_user:
                m1 = await send_message_text_to_user_handler(uuid=uuid, text=data.get("text"))
                m2 = await send_video_to_user_handler(uuid=uuid, video=data.get("video"))

                if m1 & m2:
                    count += 1
                await asyncio.sleep(.05)
        else:
            m1 = await send_message_text_to_user_handler(uuid=send_all_or_one, text=data.get("text"))
            m2 = await send_video_to_user_handler(uuid=send_all_or_one, video=data.get("video"))
    finally:
        logger.info(f"{count} messages successful sent.")
        uuids_user.clear()
    return count


async def send_quiz_from_json(chat_id: str | None,
                              text: str,
                              disable_notification: bool,
                              admin_uuid: str | None,
                              reply_markup: InlineKeyboardMarkup,
                              v: int,
                              quiz_answer: list[QuizOption]) -> int:
    """
    chat_id: id пользователя, если None то передаем всем пользователям которые входят в группу USER
    text: Текст квиза, вопрос квиза
    disable_notification: не ясный параметр, по умолчанию False
    admin_uuid: id администратора который создал квиз, если None то не посылаем квиз администратору
    reply_markup: инлайн клавиатура с вопросами квиза
    """

    uuids_user: list[str] = []
    count = 0
    if v == 1:
        text: str = f"❓ <i>{text}</i>\n\n"
    elif v == 2:
        text: str = f"❓ <i>{text}</i>\n\n"
        con = 1
        print(quiz_answer)
        for i in quiz_answer:
            text += f"<b>{EMOJI_NUM[str(con)]} {i.answer}</b>\n"
            con += 1
    if chat_id is None:
        uuids_user = await get_users_by_role(role=Roles.USER)
    else:
        uuids_user.append(chat_id)

    if admin_uuid is not None:
        uuids_user.append(admin_uuid)
    try:
        for uuid in uuids_user:
            try:
                await bot.send_message(
                    chat_id=str(uuid),
                    text=text,
                    disable_notification=disable_notification,
                    reply_markup=reply_markup, parse_mode="html"
                )
                count = count + 1
            except TelegramRetryAfter as e:
                logger.error(f"Target [ID:{uuid}]: Flood limit is exceeded. "
                             f"Sleep {e.retry_after} seconds."
                             )
                await asyncio.sleep(e.retry_after)
                await bot.send_message(
                    chat_id=str(uuid),
                    text=text,
                    disable_notification=disable_notification,
                    reply_markup=reply_markup
                )
                count = count + 1
            except TelegramForbiddenError:
                logger.info(f"Target [ID:{uuid}]: Bot Blocked")
    finally:
        logger.info(f"{count} messages successful sent.")
        print(f"{count} messages successful sent.")
        uuids_user.clear()
    return count


async def bot_answer(text: str, disable_notification: bool, reply_markup: InlineKeyboardMarkup, users: list) -> int:
    count = 0

    try:
        for uuid in users:
            try:
                await bot.send_message(
                    chat_id=str(uuid),
                    text=text,
                    disable_notification=disable_notification,
                    reply_markup=reply_markup, parse_mode="html"
                )
                count = count + 1
            except TelegramRetryAfter as e:
                logger.error(f"Target [ID:{uuid}]: Flood limit is exceeded. "
                             f"Sleep {e.retry_after} seconds."
                             )
                await asyncio.sleep(e.retry_after)

            except TelegramForbiddenError:
                logger.info(f"Target [ID:{uuid}]: Bot Blocked")
    finally:
        logger.info(f"{count} messages successful sent.")
        print(f"{count} messages successful sent.")
        users.clear()
    return count

import json

from datetime import datetime
from typing import Any

from aiogram.types import Message

from lexicon.message_constants.all_str_constants_ru import PASSWORDS
from config.app_settings import settings


def get_timestamp() -> str:
    now = datetime.now()
    ts = now.timestamp()
    ts_int = int(ts)
    return str(ts_int)


async def get_data_from_json(message: Message) -> Any:
    await message.answer(f"Отлично, я получил нужный документ.\n <i>Проверяю его корректность.</i>")
    file_info = await message.bot.get_file(message.document.file_id)
    downloaded_file = await message.bot.download_file(file_info.file_path)
    src = settings.PATH_FOR_QUIZ_FILES + get_timestamp() + "_" + message.document.file_name
    with open(src, "wb") as new_file:
        new_file.write(downloaded_file.getvalue())
    with open(src, "r") as file:
        content = file.read()
    data = json.loads(content)
    return data


def check_type_action(data: Any, type: str) -> bool:
    if type.lower() == data.get("type").lower():
        return True
    else:
        return False


def check_password_in_files(data: Any) -> bool:
    if data.get("password").lower() in PASSWORDS.values():
        return True
    else:
        return False

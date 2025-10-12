import asyncio
import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from db.crud import get_all_user_wrapper, create_admin
from db.mediacontent_crud import create_new_mediacontent
from db.poll import get_all_polls, get_all_polls_tail, get_poll_result
from keyboards.keyboards import kb_begin_or_cancel, kb_register
from lexicon.lexicon import POLL_ANSWER_TEXT
from models import MediaContent
from routers.admin_commands.bot_answer import send_list_message
from states.admin_menu_states import AdminMenuUploadvideoStates
from states.update_role_to_admin import Update_To_Admin
from config.app_settings import settings

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command(commands="uploadvideo"), StateFilter(None))
async def menu_command(message: Message, state: FSMContext):
    if str(message.from_user.id) in settings.ADMINS:
        await state.set_state(AdminMenuUploadvideoStates.begin)
        await message.answer(text="мы начинаем загрузку", reply_markup=kb_begin_or_cancel)
    else:
        await message.answer(text="Простите", parse_mode=ParseMode.HTML)


@router.message(AdminMenuUploadvideoStates.begin, F.text.lower() == "начать")
async def admin_menu_upload_video_yes(message: Message, state: FSMContext):
    await state.set_state(AdminMenuUploadvideoStates.uploadvideo)
    await message.answer(text="Перетащите или выберите видео файл")


@router.message(AdminMenuUploadvideoStates.uploadvideo, F.video)
async def admin_menu_upload_video_get(message: Message, state: FSMContext):
    mediacontent: MediaContent = MediaContent()
    mediacontent.file_id = message.video.file_id
    if message.caption is not None:
        mediacontent.file_caption = message.caption
    else:
        mediacontent.file_caption = ""
    mediacontent.file_name = message.video.file_name
    mediacontent.uuid_user_upload = str(message.from_user.id)
    mediacontent.file_type = "V"
    await state.clear()
    await create_new_mediacontent(mediacontent=mediacontent)


@router.message(AdminMenuUploadvideoStates.begin, F.text.lower() == "отмена")
async def admin_menu_upload_video_no(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Загрузка отменена")


@router.message(Command(commands="viewusers"), StateFilter(None))
async def menu_command_viewusers(message: Message):
    if str(message.from_user.id) in settings.ADMINS:
        users = await get_all_user_wrapper()
        count: int = 1
        for user in users:
            try:
                await message.answer(text=f"{count}. {user.uuid} {user.first_name} {user.last_name}")
                count = count + 1

            except TelegramRetryAfter as e:
                logger.error(f"Target: Flood limit is exceeded. "
                             f"Sleep {e.retry_after} seconds."
                             )
                await asyncio.sleep(e.retry_after)
                await message.answer(text=f"{count}. {user.uuid} {user.first_name} {user.last_name}")
                count = count + 1


@router.message(Command(commands="viewtablepoll"), StateFilter(None))
async def menu_command_viewtablepoll(message: Message):
    if str(message.from_user.id) in settings.ADMINS:
        polls = await get_all_polls()
        list_poll: list[str] = []
        for poll in polls:
            list_poll.append(f"<b>{poll.id}</b> - <i>{poll.question}</i>\n")
        await send_list_message(data=list_poll, message=message)


@router.message(Command(commands="getresultpolltail"), StateFilter(None))
async def get_result_poll_tail(message: Message):
    answer: dict = {"yes": 0, "no": 0, "none": 0}
    polls: list = await get_all_polls_tail()
    data: list = []
    for poll in polls:
        results = await get_poll_result(poll_id=poll.id)
        for result in results:
            match result[2]:
                case 0:
                    answer["yes"] = result[3]
                case 1:
                    answer["no"] = result[3]
                case -1:
                    answer["none"] = result[3]

        str_for_results: str = (f"{POLL_ANSWER_TEXT["0"]} = {answer["yes"]}\n"
                                f"{POLL_ANSWER_TEXT["1"]} = {answer["no"]}\n"
                                f"{POLL_ANSWER_TEXT["-1"]} = {answer["none"]}")

        answer.update({"yes": 0, "no": 0, "none": 0})

        data.append(f"<b>{poll.id}</b> - <i>{poll.question}</i>\n{str_for_results}")
    await send_list_message(data=data, message=message)


@router.message(Command(commands="createadmin"), StateFilter(None))
async def get_uuid_user(message: Message, state: FSMContext):
    if str(message.from_user.id) in settings.ADMINS:
        await message.answer(
            text=f"Пожалуйста введите идетнификатор пользователя которому необходимо дать права Администратора"
        )
        await state.set_state(Update_To_Admin.get_uuid)
        # data = await state.get_data()
        # await state.update_data()


@router.message(Update_To_Admin.get_uuid)
async def accept_uuid(message: Message, state: FSMContext):
    if str(message.from_user.id) in settings.ADMINS:
        await state.update_data(uuid=str(message.text.strip()))
        data = await state.get_data()
        await state.set_state(Update_To_Admin.accepted)
        await message.answer(text=f"Вы уверены в своих действиях?", reply_markup=kb_register)


@router.message(Update_To_Admin.accepted, F.text.lower() == "да")
async def accept_update(message: Message, state: FSMContext):
    if str(message.from_user.id) in settings.ADMINS:
        data = await state.get_data()
        user = await create_admin(user_uuid=data.get("uuid"))
        await message.answer(text=f"{user.uuid} {user.first_name} {user.last_name} {user.role}",
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()


@router.message(Update_To_Admin.accepted, F.text.lower() == "нет")
async def cancel_update(message: Message, state: FSMContext):
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())
    await state.clear()

import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from routers.admin_commands.bot_answer import send_video_and_text
from states.create_vidio_states import CreateVideo
from lexicon.message_constants.all_str_constants_ru import (
    POINTING_DOWN, SEND_QUIZ_ALL_OR_ONE,
)
from keyboards.keyboards import kb_cancel
from config.app_settings import settings

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command("sendvideo", prefix="!/"))
async def start_send_video(message: Message, state: FSMContext):
    await message.answer(
        f"Какое название Вы хотите дать для видео? Введите название: {POINTING_DOWN} или нажмите отмена.",
        reply_markup=kb_cancel
    )
    await state.clear()
    await state.set_state(CreateVideo.text)


@router.message(CreateVideo.text, F.text)
async def pull_text_for_video(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(CreateVideo.video)
    await message.answer(text=f"Добавте видео.", reply_markup=kb_cancel)


@router.message(CreateVideo.text)
async def error_write_text(message: Message, state: FSMContext):
    await message.answer(text=f"Введите текст {POINTING_DOWN}", reply_markup=kb_cancel)


@router.message(CreateVideo.video, F.video)
async def pull_video(message: Message, state: FSMContext):
    await state.update_data(video=message.video.file_id)
    await message.answer(text=f"Прекрасно, видео загружено, идентификатор {message.video.file_id}")
    await state.set_state(CreateVideo.end)
    data = await state.get_data()
    creator = str(message.from_user.id)
    await message.answer(text="Все готово, Отправлю Вам. Убедитесь, что все правильно")
    count = await send_video_and_text(data, admin_uuid=creator, send_all_or_one=SEND_QUIZ_ALL_OR_ONE)
    logger.info(f"Рассылка отправлена {count} пользователям")
    await message.answer(text="Что будем делать?", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Отправить', callback_data='sendvideo'),
                InlineKeyboardButton(text='Отменить', callback_data='quit'),
            ]
        ]
    ))


@router.callback_query(CreateVideo.end, F.data == "sendvideo")
async def send_mailing(callback: CallbackQuery, state: FSMContext):
    send_data = await state.get_data()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(text="Отправляю >>>>>>>>", reply_markup=None)
    if settings.SEND_MAILING_ALL:
        count = await send_video_and_text(data=send_data, admin_uuid=None, send_all_or_one=SEND_QUIZ_ALL_OR_ONE)
        logger.info(f"Рассылка отправлена {count} пользователям")
        await callback.message.answer(f"Рассылка отправлена {count} пользователям")
    else:
        await callback.message.answer(f"Рассылка УСЛОВНО отправлена  пользователям")
    await state.clear()


@router.message(CreateVideo.video)
async def error_pull_video(message: Message, state: FSMContext):
    await message.answer(text=f"Пожалуйста, только видео контент.", reply_markup=kb_cancel)


@router.callback_query(CreateVideo.text, F.data == "quit")
@router.callback_query(CreateVideo.video, F.data == "quit")
@router.callback_query(CreateVideo.end, F.data == "quit")
async def quit_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.clear()
    await callback.message.answer(text=f"Создание рассылки отменено.")

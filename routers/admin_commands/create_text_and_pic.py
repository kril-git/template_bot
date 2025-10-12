import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram import html
from keyboards.keyboards import kb_add_photo
from states.create_text_and_pic_states import CreateTextAndPic
from lexicon.message_constants.all_str_constants_ru import (THINKING_FACE,
                                       FOLDED_HANDS,
                                       POINTING_DOWN,
                                       A_CHOICE_PHOTO,
                                       )
from routers.admin_commands.bot_answer import send_photo_and_text
from config.app_settings import settings

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command(commands="mailing", prefix="!/"))
async def start_mailing(message: Message, state: FSMContext):
    await message.answer(f"Введите текст рассылки:")
    await state.set_state(CreateTextAndPic.text)


@router.message(CreateTextAndPic.text, F.text)
async def mailing_text(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(text=answer)
    await state.set_state(CreateTextAndPic.state)
    result = await message.answer(
        text=A_CHOICE_PHOTO, parse_mode=ParseMode.HTML,
        reply_markup=kb_add_photo())


@router.message(CreateTextAndPic.text)
async def err_mailing_text(message: Message):
    await message.answer(text=f"{THINKING_FACE} Не совсем то что я ожидал, пожалуйста введите текст. {FOLDED_HANDS}")


@router.callback_query(CreateTextAndPic.state, F.data == "add_photo")
async def add_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Выберите фотографию для рассылки.")
    await state.set_state(CreateTextAndPic.photo)


@router.callback_query(CreateTextAndPic.state, F.data == "next")
async def skip_photo(callback: CallbackQuery, state: FSMContext):
    await state.update_data(photo="none")
    await state.set_state(CreateTextAndPic.text_message)
    await callback.message.delete_reply_markup()
    await callback.message.answer(text=f"Проигнорируем фотографию))) -> Введите текст. {POINTING_DOWN}")


@router.callback_query(CreateTextAndPic.photo, F.data == "next")
async def entry_text(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CreateTextAndPic.text_message)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(text=f"Введите текст. {POINTING_DOWN}", reply_markup=ReplyKeyboardRemove())


@router.callback_query(CreateTextAndPic.end, F.data == "sendmailing")
async def send_mailing(callback: CallbackQuery, state: FSMContext):
    send_data = await state.get_data()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(text="Отправляю >>>>>>>>", reply_markup=None)
    if settings.SEND_MAILING_ALL:
        count = await send_photo_and_text(data=send_data, admin_uuid=None)
        logger.info(f"Рассылка отправлена {count} пользователям")
        await callback.message.answer(f"Рассылка отправлена {count} пользователям")
    else:
        await callback.message.answer(f"Рассылка УСЛОВНО отправлена  пользователям")
    await state.clear()


@router.message(CreateTextAndPic.text_message, F.text)
async def write_text(message: Message, state: FSMContext):
    await state.update_data(mailing_text=message.text)
    await state.set_state(CreateTextAndPic.end)
    data = await state.get_data()
    creator = str(message.from_user.id)
    await message.answer(text="Все готово, Отправлю Вам. Убедитесь, что все правильно")
    count = await send_photo_and_text(data, admin_uuid=creator)
    logger.info(f"Рассылка отправлена {count} пользователям")
    await message.answer(text="Что будем делать?", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Отправить', callback_data='sendmailing'),
                InlineKeyboardButton(text='Отменить', callback_data='quit'),
            ]
        ]
    ))


@router.message(CreateTextAndPic.text_message)
async def skip_photo(message: Message, state: FSMContext):
    await message.answer(text=f"Введите текст. {POINTING_DOWN}", reply_markup=ReplyKeyboardRemove())


@router.message(CreateTextAndPic.state)
async def err_choice(message: Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=int(message.message_id - 1))
    await message.answer(text=POINTING_DOWN, reply_to_message_id=message.message_id, reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text=A_CHOICE_PHOTO, parse_mode=ParseMode.HTML,
        reply_markup=kb_add_photo())


@router.message(CreateTextAndPic.photo, F.photo)
async def mailing_text(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Далее', callback_data='next'),
                InlineKeyboardButton(text='Отменить', callback_data='quit'),
            ]
        ]
    )
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)


@router.message(CreateTextAndPic.photo)
async def no_photo(message: Message, state: FSMContext):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Отменить', callback_data='quit')
            ]
        ]
    )
    await message.answer(text=f"Что то пошло не так, жду от тебя {html.bold("фотографию")}\n"
                              f"{html.bold("ИЛИ")}\n"
                              f"Нажми {html.bold("Отменить")} для отказа от рассылки.", reply_markup=markup)


@router.callback_query(StateFilter(CreateTextAndPic.state), F.data == "quit")
@router.callback_query(StateFilter(CreateTextAndPic.text), F.data == "quit")
@router.callback_query(StateFilter(CreateTextAndPic.photo), F.data == "quit")
@router.callback_query(StateFilter(CreateTextAndPic.end), F.data == "quit")
async def quit_mailing(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete_reply_markup()
    await callback.message.answer('Рассылка отменена.')

import random

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.crud import if_exist_user_by_uuid, create_new_user, get_user_by_uuid, update_last_visit_user_by_id
from handlers.handlers import logger
from init import bot
from keyboards import keyboards as kb
from lexicon.lexicon import LEXICON_COMMANDS_ADMIN_MENU, LEXICON_COMMANDS_ADMIN
from models import User
from states.registration_question import RegistrationQuestion
from lexicon.message_constants.all_str_constants_ru import A_HELP_FOR_USER, A_ERROR_MESSAGE_ANSVER
from config.app_settings import settings

router = Router(name=__name__)


@router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    if_exist = await if_exist_user_by_uuid(uuid=str(message.from_user.id))
    if not if_exist:
        user = User()
        user.uuid = str(message.from_user.id)
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
        new_user = await create_new_user(user=user)
        logger.info(f"Создан пользователь с UUID = {new_user.uuid}")
        await message.answer('Привет друг!')
        await message.answer('Я кратко расскажу о этом проекте и о том как нам лучше взаимодействовать!')
        await message.answer('Для начала давай ответим на несколько вопросов!')
        await state.set_state(RegistrationQuestion.question)
        await message.answer('ГОТОВ?', parse_mode="HTML", reply_markup=kb.kb_register)

    else:  # пользователь существует
        # добавить меню
        if str(message.from_user.id) in settings.ADMINS:
            pass
        else:
            pass

        await message.answer('Привет, рад снова тебя видеть у себя на канале')  # можно добавить генератор сообщений
        user = await get_user_by_uuid(uuid=str(message.from_user.id))
        await update_last_visit_user_by_id(user=user)
        if not user.registration:  # пользователь не зарегистрирован
            await message.answer('Давай попробуем снова ответить на пару вопросов)))')
            await state.set_state(RegistrationQuestion.question)
            await message.answer('ГОТОВ? \U0001f600 Жми на кнопочку \U0001F447', parse_mode="HTML",
                                 reply_markup=kb.kb_register)
        else:  # пользователь зарегистрирован
            pass


@router.message(Command(commands="help", prefix="/"), StateFilter(None))
async def help_command(message: Message):
    if str(message.from_user.id) in settings.ADMINS:
        text: str = ""
        for key, value in LEXICON_COMMANDS_ADMIN.items():
            text += f"{key} : <i>{value}</i>\n"
        await message.answer(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.answer(text=A_HELP_FOR_USER, parse_mode=ParseMode.HTML)


@router.message(Command(commands="menu", prefix="/"), StateFilter(None))
async def menu_command(message: Message):
    if str(message.from_user.id) in settings.ADMINS:
        text: str = ""
        for key, value in LEXICON_COMMANDS_ADMIN_MENU.items():
            text += f"{key} : <i>{value}</i>\n"
        await message.answer(text=text)
    else:
        await message.answer(text="Простите", parse_mode=ParseMode.HTML)


@router.message(F.text)
async def echo_message(message: Message, state: FSMContext):
    # await state.clear()
    # await bot.send_message(message.from_user.id, message.text)
    await bot.send_message(message.from_user.id, random.choice(A_ERROR_MESSAGE_ANSVER))
    print(message.text)

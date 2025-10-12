from aiogram import Router, F, types
import logging

from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown

from common.validation import validate_age
from db.registration_crud import update_reg_info_user
from filters.gender_filters import IsGender
from keyboards import keyboards as kb
from keyboards.keyboards import kb_gender
from states.registratio_question_full import RegistrationQuestionFull
from states.registration_question import RegistrationQuestion
from utils.EGender import Genders
from lexicon.message_constants.yes_or_no import YesOrNo
from lexicon.message_constants.all_str_constants_ru import (
    Q_AGE,
    Q_GENDER,
    A_ERROR_TRY_AGAIN,
    A_SECS_FEMALE,
    A_SECS_MALE, BEGIN_VIDEO_ID_ANSWER
)

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationQuestionFull.nic_name, F.text)
async def read_nic_name(message: Message, state: FSMContext):
    await message.answer(
        f"Я могу обращаться к тебе как {markdown.hbold(message.text[0].upper() + message.text[1:].lower())}?",
        parse_mode=ParseMode.HTML,
        reply_markup=kb.kb_register,
    )
    await state.update_data(name=message.text[0].upper() + message.text[1:].lower())
    await state.set_state(RegistrationQuestionFull.yes_or_no)


@router.message(RegistrationQuestionFull.yes_or_no, F.text.lower() == YesOrNo.YES.value.lower())
async def read_nic_name_success(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Прекрасно!!! {data.get("name")}", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(Q_AGE)
    await state.set_state(RegistrationQuestionFull.age)


@router.message(RegistrationQuestionFull.age, F.text)
async def read_age(message: Message, state: FSMContext):
    if validate_age(message.text):
        # data = await state.get_data()
        await state.update_data(age=int(message.text))
        await state.set_state(RegistrationQuestionFull.gender)
        await message.answer(f"{Q_GENDER}", reply_markup=kb_gender)
    else:
        print("увы")
        await message.answer(f"Мне кажется ты ошибся, попробуй снова)) {Q_AGE}")


@router.callback_query(RegistrationQuestionFull.gender, IsGender(Genders))
async def read_answer_gender(callback: CallbackQuery, state: FSMContext):
    gender = Genders(int(callback.data)).name
    user_data = await state.get_data()
    match gender:
        case Genders.MALE.name:
            await state.update_data(gender=Genders.MALE.name)
            await callback.message.answer(f"{A_SECS_MALE} {user_data.get("name")}")
        case Genders.FEMALE.name:
            await state.update_data(gender=Genders.FEMALE.name)
            await callback.message.answer(f"{A_SECS_FEMALE} {user_data.get("name")}")
    await state.update_data(uuid=callback.from_user.id)
    user_data = await state.get_data()
    await update_reg_info_user(data=user_data)

    await callback.message.delete()
    await state.clear()

    # скорее всего тут надо добавить вступительное слово
    # video_file = FSInputFile(path=os.path.join(settings.PATH_FOR_ALL_MEDIA_FILES, '1.MOV'))
    # await bot.send_video(
    #         chat_id=callback.from_user.id,
    #         video=BEGIN_VIDEO_ID_ANSWER
    #     )
    # предварительно надо грузить видео на сервер и получать его ИД
    try:
        await callback.message.answer_video(video=BEGIN_VIDEO_ID_ANSWER)
    except TelegramBadRequest as e:
        logger.error(f"TelegramBadRequest: {e}. нет видео на сервере Телеграм.")
        print(f"ERROR --->>> TelegramBadRequest: {e}. нет видео на сервере Телеграм.")

@router.message(RegistrationQuestionFull.gender)
async def error_answer_gender(message: Message, state: FSMContext):
    await message.answer(A_ERROR_TRY_AGAIN)


@router.message(RegistrationQuestion.question, F.text.lower() == YesOrNo.NO.value.lower())
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Почитайте тогда новости', reply_markup=types.ReplyKeyboardRemove())


@router.message(RegistrationQuestion.question, F.text.lower() == YesOrNo.YES.value.lower())
async def registration(message: Message, state: FSMContext):
    # await state.clear()
    await message.answer('Ты нажал ДААААА', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegistrationQuestionFull.nic_name)
    await message.answer(text='Как я могу к тебе обращаться?')


@router.message(RegistrationQuestion.question)
async def error_answer(message: Message,):
    await message.answer("Пожалуйста...")

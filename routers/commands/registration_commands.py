from aiogram import Router, F, types
import logging

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown

from common.validation import validate_age
from db.registration_crud import update_reg_info_user
from filters.gender_filters import IsGender
from keyboards import keyboards as kb
from keyboards.keyboards import kb_gender
from states.registratio_question_full import RegistrationQuestionFull
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
    # user = await get_user_by_uuid(uuid=str(message.from_user.id))
    # data = await state.get_data()
    # user.nic_name = data.get("name")
    # print(data.get("name"))

    # await state.set_state(RegistrationQuestionFull.age)
    await message.answer(Q_AGE)
    await state.set_state(RegistrationQuestionFull.age)
    # await state.update_data(age=message.text)
    # print(message.text)
    # await state.clear()

    # data= await state.get_data()
    # print(data)


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
# @router.callback_query(RegistrationQuestionFull.gender, F.data == str(Genders.FEMALE.value) or str(Genders.MALE.value))
# @router.callback_query(RegistrationQuestionFull.gender, F.data == str(Genders.MALE.value))
async def read_answer_gender(callback: CallbackQuery, state: FSMContext):
    # print(type(callback.data), f"{type(Genders.MALE.value)}, {Genders.FEMALE.value}")
    # print(Genders(int(callback.data)).name)
    # gender = Genders(int(callback.data)).name
    # if Genders(int(callback.data)).name == None:
    #     gender = Genders.MALE.name
    # else:
    gender = Genders(int(callback.data)).name
    user_data = await state.get_data()
    print(f"--------------------->>>>   {Genders(int(callback.data)).name}  <<<--------------")
    match gender:
        case Genders.MALE.name:
            await state.update_data(gender=Genders.MALE.name)
            await callback.message.answer(f"{A_SECS_MALE} {user_data.get("name")}")
        case Genders.FEMALE.name:
            await state.update_data(gender=Genders.FEMALE.name)
            await callback.message.answer(f"{A_SECS_FEMALE} {user_data.get("name")}")
    # user_data = await state.get_data()
    await state.update_data(uuid=callback.from_user.id)
    user_data = await state.get_data()
    await update_reg_info_user(data=user_data)

    print(user_data, callback.from_user.id)
    await callback.message.delete()
    await state.clear()

    # скорее всего тут надо добавить вступительное слово
    # video_file = FSInputFile(path=os.path.join(settings.PATH_FOR_ALL_MEDIA_FILES, '1.MOV'))
    # await bot.send_video(
    #         chat_id=callback.from_user.id,
    #         video=BEGIN_VIDEO_ID_ANSWER
    #     )

    await callback.message.answer_video(video=BEGIN_VIDEO_ID_ANSWER)

@router.message(RegistrationQuestionFull.gender)
async def error_answer_gender(message: Message, state: FSMContext):
    await message.answer(A_ERROR_TRY_AGAIN)

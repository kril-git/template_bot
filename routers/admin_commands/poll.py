import logging

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from common.function import get_data_from_json, check_type_action, check_password_in_files
from db.poll import create_poll, get_poll_title, if_user_end_poll, create_poll_answer
from keyboards.kbd_bilders import create_kbd_for_poll, PollCallbackFactory
from keyboards.keyboards import kb_quiz_push
from routers.admin_commands.send_poll import send_poll_from_json
from states.create_poll_from_json import CreatePollFromJson
from lexicon.message_constants.all_str_constants_ru import EMOJI_ALL, SEND_QUIZ_ALL_OR_ONE
from config.app_settings import settings

from lexicon.lexicon import LEXICON

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command(commands="poll", prefix="!/"), StateFilter(None))
async def start_mailing(message: Message, state: FSMContext):
    if str(message.from_user.id) in settings.ADMINS:
        await state.set_state(CreatePollFromJson.begin)
        await message.answer(LEXICON["/poll"])
    else:
        await state.clear()


@router.message(F.content_type == ContentType.DOCUMENT, CreatePollFromJson.begin)
async def load_poll_json_file(message: Message, state: FSMContext):
    if message.document.mime_type == "application/json":
        data = await get_data_from_json(message)
        if check_type_action(data=data, type="poll"):
            await message.answer(text=f"Отлично, тип соответствует ожиданию. {EMOJI_ALL["OK"]}\n")
            if check_password_in_files(data=data):
                await message.answer(text=f"Файл прошел проверку, записываю данные в БД.\n ")
                result = await create_poll(data=data, uuid=str(message.from_user.id))
                if result != -1:
                    await message.answer("Отлично, пока все идет так как надо))")
                    await state.update_data(poll_id=result)
                    await state.update_data(version=data.get("v"))
                    await state.set_state(CreatePollFromJson.push)
                    await message.answer("Примите решение)))", reply_markup=kb_quiz_push)
                else:
                    pass
            else:
                await message.answer(text=f"Что то не так, <b>пароль</b> в файле не совпадает((, попробуйте все с "
                                          f"начала.")
                await state.clear()
        else:
            await message.answer(text=f"Я ожидаю тип действия quiz (проверь JSON поле type). Попробуй все с начала")
            await state.clear()
    else:
        await message.answer(text=f"Я ожидаю JSON файл.")


@router.message(F.text.contains("Отправить"), CreatePollFromJson.push)
async def push_poll(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Прекрасно отправляю!!! id опроса = {data.get("poll_id")}\nверсия = {data.get("version")}",
                         reply_markup=ReplyKeyboardRemove())
    poll_id = data.get("poll_id")
    poll = await get_poll_title(poll_id=poll_id)

    """
    отправляю опрос пользователю одному для проверки или всем пользователям
    """
    await state.clear()
    if data.get("version") == 1:
        await send_poll_from_json(
            chat_id=SEND_QUIZ_ALL_OR_ONE,
            text=poll.question,
            disable_notification=False,
            admin_uuid=str(message.from_user.id),
            reply_markup=create_kbd_for_poll(poll_id=int(poll_id), v=data.get("version")),
            v=data.get("version"),
        )


@router.message(F.text.contains("Отмена"), CreatePollFromJson.push)
# @router.message(F.text.contains("Отмена"), Test.push)
async def cancel_quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"Опрос не будет проведен, id опроса -> {data.get("poll_id")}. Данные сохранены в базу данных. Возможно в "
        f"скором времени появится сервис который повторно позволит запустить опрос по ID.",
        reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.callback_query(StateFilter(None), PollCallbackFactory.filter())
async def callback_quiz_callback(callback_query: CallbackQuery, callback_data: PollCallbackFactory):
    # нужно создать запись в базе в таблице quizanswer
    if not await if_user_end_poll(user_id=str(callback_query.from_user.id), poll_id=callback_data.poll_id):
        poll_answer_data: dict = {"poll_id": callback_data.poll_id,
                                  "user_id": callback_query.from_user.id,
                                  "user_answer": callback_data.answer_number,
                                  "poll_end": True,
                                  }
        print("------------------->>>>>>>>>>")
        print(poll_answer_data.items())
        if await create_poll_answer(data=poll_answer_data):
            await callback_query.message.delete_reply_markup()
            await callback_query.message.answer(text=EMOJI_ALL["OK"])

    else:
        await callback_query.message.answer(text="Вы уже приняли участие в этом опросе)))")


@router.message(Command(commands="cancel", prefix="!/"), CreatePollFromJson.begin)
async def cancel_pool(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["/cancel_poll"])
    await state.clear()

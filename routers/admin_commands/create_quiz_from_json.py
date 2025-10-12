import logging

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from db.quiz import create_quiz, get_quiz_answer_by_id, get_quiz_title, get_quiz_correct_answer, \
    create_quiz_answer, if_user_end_quiz, get_quiz_correct_answer_by_id
from keyboards.kbd_bilders import create_kbd_for_quiz, QuizCallbackFactory, edit_kbd_for_quiz, create_kbd_for_quiz_v2, \
    edit_kbd_for_quiz_v2
from keyboards.keyboards import kb_quiz_push
from states.create_quiz_from_json import CreateQuizFromJson
from states.test import Test
from routers.admin_commands.bot_answer import send_quiz_from_json
from lexicon.message_constants.all_str_constants_ru import SEND_QUIZ_ALL_OR_ONE, EMOJI_NUM, EMOJI_ALL
from config.app_settings import settings
from common.function import get_data_from_json, check_type_action, check_password_in_files

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(Command(commands="quizjson", prefix="!/"), StateFilter(None))
async def start_mailing(message: Message, state: FSMContext):
    if str(message.from_user.id) in settings.ADMINS:
        await state.set_state(CreateQuizFromJson.begin)
        await message.answer(f"Жду JSON файл квиза или /cancel для отмены действий:")
    else:
        await state.clear()


@router.message(F.content_type == ContentType.DOCUMENT, CreateQuizFromJson.begin)
async def load_quiz_json_file(message: Message, state: FSMContext):
    if message.document.mime_type == "application/json":
        data = await get_data_from_json(message)
        if check_type_action(data=data, type="quiz"):
            await message.answer(text=f"Отлично, тип соответствует ожиданию. {EMOJI_ALL["OK"]}\n")
            if check_password_in_files(data=data):
                await message.answer(text=f"Файл прошел проверку, записываю данные в БД.\n ")
                result = await create_quiz(data=data, uuid=str(message.from_user.id))
                if result != -1:
                    await message.answer("Отлично, пока все идет так как надо))")
                    await state.update_data(quiz_id=result)
                    await state.update_data(version=data.get("v"))
                    await state.set_state(CreateQuizFromJson.push)
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


@router.message(CreateQuizFromJson.begin)
async def echo_pull_quiz(message: Message):
    await message.answer(f"Жду JSON")


@router.message(F.text.contains("Отправить"), CreateQuizFromJson.push)
@router.message(F.text.contains("Отправить"), Test.push)
async def push_quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Прекрасно отправляю!!! id квиза = {data.get("quiz_id")}\nверсия = {data.get("version")}",
                         reply_markup=ReplyKeyboardRemove())
    quiz_id = data.get("quiz_id")
    quiz = await get_quiz_title(quiz_id=quiz_id)
    quiz_answer = await get_quiz_answer_by_id(quiz_id=quiz_id)

    # отправляю квиз пользователю одному для проверки или всем пользователям
    await state.clear()
    if data.get("version") == 1:
        await send_quiz_from_json(
            chat_id=SEND_QUIZ_ALL_OR_ONE,
            text=quiz.question,
            disable_notification=False,
            admin_uuid=str(message.from_user.id),
            reply_markup=create_kbd_for_quiz(answer=quiz_answer, quiz_id=int(quiz_id), v=data.get("version")),
            v=data.get("version"),
            quiz_answer=quiz_answer,
        )
    elif data.get("version") == 2:
        await send_quiz_from_json(
            chat_id=SEND_QUIZ_ALL_OR_ONE,
            text=quiz.question,
            disable_notification=False,
            admin_uuid=str(message.from_user.id),
            reply_markup=create_kbd_for_quiz_v2(answer=quiz_answer, quiz_id=int(quiz_id), v=data.get("version")),
            v=data.get("version"),
            quiz_answer=quiz_answer,

        )


@router.message(F.text.contains("Отмена"), CreateQuizFromJson.push)
@router.message(F.text.contains("Отмена"), Test.push)
async def cancel_quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"Рассылка не будет проведена, id квиза -> {data.get("quiz_id")}. Данные сохранены в базу данных. Возможно в "
        f"скором времени появится сервис который поторый позволит запустить квиз по ID.",
        reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command(commands="cancel"), StateFilter(CreateQuizFromJson))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await state.get_state()
    await message.answer("Действие отменено")


@router.callback_query(StateFilter(None), QuizCallbackFactory.filter())
async def callback_quiz_callback(callback_query: CallbackQuery, callback_data: QuizCallbackFactory):
    correct_answer_id = await get_quiz_correct_answer(quiz_id=callback_data.quiz_id)

    # нужно создать запись в базе в таблице quizanswer
    if not await if_user_end_quiz(user_id=str(callback_query.from_user.id), quiz_id=callback_data.quiz_id):
        quiz_answer_data: dict = {"quiz_id": callback_data.quiz_id,
                                  "user_id": callback_query.from_user.id,
                                  "user_answer": callback_data.answer_number,
                                  "quiz_end": True,
                                  }
        if callback_data.yes == 1:
            quiz_answer_data["yes"] = True
            await callback_query.message.answer(text="ДАААА", message_effect_id="5046509860389126442")
            await callback_query.answer()
        else:
            quiz_answer_data["yes"] = False
            await callback_query.message.answer(text="Ну НЕЕТ же", message_effect_id="5046589136895476101")
            await callback_query.answer()

        await create_quiz_answer(data=quiz_answer_data)
        if callback_data.v == 1:
            new_kb = await edit_kbd_for_quiz(
                quiz_id=callback_data.quiz_id,
                user_answer=callback_data.answer_number,
                correct_answer=correct_answer_id
            )
        elif callback_data.v == 2:
            new_kb = await edit_kbd_for_quiz_v2(
                quiz_id=callback_data.quiz_id,
                user_answer=callback_data.answer_number,
                correct_answer=correct_answer_id
            )
        correct_answer = await get_quiz_correct_answer_by_id(quiz_id=quiz_answer_data["quiz_id"])
        await callback_query.message.edit_reply_markup(reply_markup=new_kb, parse_mode="HTML")
        # await callback_query.message.edit_text(text="dedeedededdedde", reply_markup=new_kb)
        # await callback_query.message.message_id
        if callback_data.v == 1:
            await callback_query.message.reply(correct_answer, message_effect_id="5104841245755180586")
        elif callback_data.v == 2:
            await callback_query.message.answer(f"{EMOJI_NUM[str(correct_answer_id + 1)]} {correct_answer}",
                                                message_effect_id="5104841245755180586")

    else:
        await callback_query.message.answer(text="Вы уже приняли участие в этом квизе)))")


@router.callback_query(F.data == "None")
async def callback_(callback_query: CallbackQuery):
    await callback_query.message.answer(text="Вы уже приняли участие в этом квизе)))")

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.quiz import get_quiz_answer_by_id
from lexicon.lexicon import POLL_ANSWER_TEXT
from models import QuizOption
from lexicon.message_constants.all_str_constants_ru import EMOJI_NUM


# builder = InlineKeyboardBuilder() 1️⃣2️⃣3️⃣4️⃣🎲 &#49;&#65039;&#8419;

class QuizCallbackFactory(CallbackData, prefix='quiz_callback'):
    quiz_id: int
    answer_number: int
    yes: int  # 1 если правильный ответ, 0 если нет
    v: int


class PollCallbackFactory(CallbackData, prefix='poll_callback'):
    poll_id: int
    answer_number: int
    v: int


def create_kbd_for_quiz(answer: list[QuizOption], quiz_id: int, v: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    count = 0
    correct_answer: int
    for option in answer:
        if option.correct_option_id:
            correct_answer = 1
        else:
            correct_answer = 0
        builder.button(text=option.answer, callback_data=QuizCallbackFactory(
            quiz_id=quiz_id,
            answer_number=option.option_id,
            yes=correct_answer,
            v=v
        ).pack()
                       )
        count = count + 1
    builder.adjust(1)
    return builder.as_markup()


def create_kbd_for_poll(poll_id: int, v: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, value in POLL_ANSWER_TEXT.items():
        builder.button(text=value, callback_data=PollCallbackFactory(
            poll_id=poll_id,
            answer_number=int(key),
            v=v
        ).pack()
                       )
    builder.adjust(1)
    return builder.as_markup()

async def edit_kbd_for_quiz(quiz_id: int, user_answer: int, correct_answer: int) -> InlineKeyboardMarkup:
    answer: list[QuizOption] = await get_quiz_answer_by_id(quiz_id=quiz_id)
    builder = InlineKeyboardBuilder()
    if user_answer == correct_answer:
        for option in answer:
            if option.option_id == user_answer:
                builder.button(text=f'✅ {option.answer}', callback_data="None")
            else:
                builder.button(text=f"❌ {option.answer}", callback_data="None")
    else:
        for option in answer:
            if option.option_id == user_answer:
                builder.button(text=f"❌ {option.answer} ❌", callback_data="None")
            elif option.option_id == correct_answer:
                builder.button(text=f'✅ {option.answer}', callback_data="None")
            else:
                builder.button(text=f"❌ {option.answer}", callback_data="None")
    builder.adjust(1)
    return builder.as_markup()


def create_kbd_for_quiz_v2(answer: list[QuizOption], quiz_id: int, v: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    count = 0
    correct_answer: int
    for option in answer:
        if option.correct_option_id:
            correct_answer = 1
        else:
            correct_answer = 0
        builder.button(text=EMOJI_NUM[str(count + 1)], callback_data=QuizCallbackFactory(
            quiz_id=quiz_id,
            answer_number=option.option_id,
            yes=correct_answer,
            v=v
        ).pack()
                       )
        count = count + 1
    builder.adjust(4)
    return builder.as_markup()


async def edit_kbd_for_quiz_v2(quiz_id: int, user_answer: int, correct_answer: int) -> InlineKeyboardMarkup:
    answer: list[QuizOption] = await get_quiz_answer_by_id(quiz_id=quiz_id)
    builder = InlineKeyboardBuilder()
    count: int = 1
    if user_answer == correct_answer:
        for option in answer:
            if option.option_id == user_answer:
                builder.button(text=f'✅ {EMOJI_NUM[str(count)]}', callback_data="None")
            else:
                builder.button(text=f"❌ {EMOJI_NUM[str(count)]}", callback_data="None")
            count += 1
    else:
        for option in answer:
            if option.option_id == user_answer:
                builder.button(text=f"❌ {EMOJI_NUM[str(count)]} ❌", callback_data="None")
            elif option.option_id == correct_answer:
                builder.button(text=f'✅ {EMOJI_NUM[str(count)]}', callback_data="None")
            else:
                builder.button(text=f"❌ {EMOJI_NUM[str(count)]}", callback_data="None")
            count += 1
    builder.adjust(4)
    return builder.as_markup()

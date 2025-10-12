from aiogram.fsm.state import State, StatesGroup


class CreateQuizFromJson(StatesGroup):
    begin = State()
    push = State()
    getfile = State()
    loadfile = State()
    next = State()
    cancel = State()
    text_message = State()
    end = State()

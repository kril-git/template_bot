from aiogram.fsm.state import State, StatesGroup


class CreateTextAndPic(StatesGroup):
    text = State()
    state = State()
    photo = State()
    next = State()
    cancel = State()
    text_message = State()
    end = State()


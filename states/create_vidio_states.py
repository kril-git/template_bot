from aiogram.fsm.state import State, StatesGroup


class CreateVideo(StatesGroup):
    text = State()
    video = State()
    end = State()

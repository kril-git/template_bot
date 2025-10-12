from aiogram.fsm.state import State, StatesGroup


class Test(StatesGroup):
    begin = State()
    push = State()
    temp = State()
    end = State()
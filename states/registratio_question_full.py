from aiogram.fsm.state import State, StatesGroup


class RegistrationQuestionFull(StatesGroup):
    nic_name = State()
    yes_or_no = State()
    age = State()
    gender = State()

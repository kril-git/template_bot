from aiogram.fsm.state import State, StatesGroup


class RegistrationQuestion(StatesGroup):
    question = State()

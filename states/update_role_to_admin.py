from aiogram.fsm.state import State, StatesGroup


class Update_To_Admin(StatesGroup):
    get_uuid = State()
    accepted = State()
    update_bd = State()
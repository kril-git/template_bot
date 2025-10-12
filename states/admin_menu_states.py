from aiogram.fsm.state import State, StatesGroup


class AdminMenuUploadvideoStates(StatesGroup):
    begin = State()
    uploadvideo = State()
    cancel = State()

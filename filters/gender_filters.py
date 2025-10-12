import enum

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from utils.EGender import Genders


class IsGender(BaseFilter):
    def __init__(self, genders: enum) -> None:
        self.genders = genders

    async def __call__(self, message: CallbackQuery):
        if message.data == str(Genders.FEMALE.value) or str(Genders.MALE.value):
            return True
        else:
            return False


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.formatting import as_line, Bold, Italic
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from utils.EGender import Genders

'''
ReplyKeyboardMarkup - клавиатура которая в низу бота. Она отправляет сообщение боту
InlineKeyboardMarkup - клавиатура под сообщением, не возвращает сообщение боту
'''

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Наши услуги')],
                                     #  [KeyboardButton(text='Корзина')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню ...')
content = as_line("✅ ", Italic("Summary:"))

catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(**content.as_kwargs(), callback_data='t-shirt')],
                                                [InlineKeyboardButton(text='Кроссовки', callback_data='sneakers')],
                                                [InlineKeyboardButton(text='Носки', callback_data='cap')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер телефона',
                                                           request_contact=True)]],
                                 resize_keyboard=True)

temp_list_calendar = [[KeyboardButton(text='Navigation Calendar'), KeyboardButton(text='Navigation Calendar w month')],
                      [KeyboardButton(text='Dialog Calendar'), KeyboardButton(text='Dialog Calendar w year'),
                       KeyboardButton(text='Dialog Calendar w month')]]

start_kb = ReplyKeyboardMarkup(keyboard=temp_list_calendar, resize_keyboard=True)


def create_keyboard_day():
    builder = InlineKeyboardBuilder()
    for i in range(12):
        builder.button(text=str(i + 9), callback_data='time' + ' ' + str(i + 9))

    return builder.as_markup()


create_keyboard_day()

kb_keybord_day = create_keyboard_day()
# ReplyKeyboardMarkup(keyboard=keyboard_day, resize_keyboard=True)

# Trinity

kb_register = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='НЕТ'), KeyboardButton(text='ДА')]],
                                  resize_keyboard=True)

kb_quiz_push = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить Квиз?"),
     KeyboardButton(text="Отмена")]
], resize_keyboard=True, one_time_keyboard=True)

kb_gender = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Мужской', callback_data=Genders.MALE)],
                                                  [InlineKeyboardButton(text='Женский', callback_data=Genders.FEMALE)]])


def kb_add_photo() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text="Добавить фотографию?", callback_data="add_photo"))
    markup.add(InlineKeyboardButton(text="Далее", callback_data="next"))
    markup.add(InlineKeyboardButton(text='Отменить', callback_data='quit'))
    markup.adjust(1, 2)
    return markup.as_markup()


kb_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Отменить', callback_data='quit')
    ]
]
)
# End Trinity

kb_services = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Услуга 1', callback_data='s1')],
                                                    [InlineKeyboardButton(text='Услуга 2', callback_data='sneakers')],
                                                    [InlineKeyboardButton(text='Услуга 3', callback_data='cap')]])

kb_cal = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Выберите дату', callback_data='get_date')]])


kb_begin_or_cancel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Начать"),
     KeyboardButton(text="Отмена")]
], resize_keyboard=True, one_time_keyboard=True)
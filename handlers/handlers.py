# import logging
#
# from aiogram import F, Router
# from aiogram.types import Message, CallbackQuery
# from aiogram.fsm.context import FSMContext
# from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
#     get_user_locale
# from aiogram.filters.callback_data import CallbackData
# from datetime import datetime
#
# import keyboards.keyboards as kb
# import states.states as st
#
# router = Router(name=__name__)
# logger = logging.getLogger(__name__)
#
#
# # @router.message(Command('nav'))
# # async def nav_cal_handler(message: Message):
# #     await message.answer(
# #         "Please select a date: ",
# #         reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
# #     )
# #     await message.answer('Введите ваше имя')
# #     print('dcddcdcdcdcdcdcdcdcdcdcdcc')
#
# # @router.message(F.text == 'дааа')
# # async def catalog(message: Message):
# #     await message.answer('Выберите категорию товара', reply_markup=kb.catalog)
#
#
# @router.message(F.text == 'Каталог')
# async def catalog(message: Message):
#     await message.answer('Выберите категорию товара', reply_markup=kb.catalog)
#
#
# @router.message(F.text.contains('услуги'))
# async def get_services(message: Message):
#     await message.answer('Выберите интересующую услугу', reply_markup=kb.kb_services)
#
#
# @router.callback_query(F.data == 'cap')
# async def get_calendar(callback: CallbackQuery):
#     print(callback.model_dump_json(indent=4, exclude_none=True))
#     await callback.answer()
#
#
# @router.callback_query(F.data == 's1')
# async def t_shirt(callback: CallbackQuery):
#     # await callback.answer('Вы выбрали Услугу 1', reply_markup=kb.kb_cal)
#     await callback.message.answer('Вы выбрали Услугу 1', reply_markup=kb.kb_cal)
#
#
# @router.callback_query(F.data == 'get_date')
# async def get_tate(callback: CallbackQuery):
#     await callback.message.answer("Please select a date: ",
#                                   reply_markup=await SimpleCalendar().start_calendar())
#     await callback.message.delete()
#     # await callback.answer('Вы выбрали Услугу 1', show_alert=True)
#
#
# @router.callback_query(F.data.contains('time'))
# async def get_time(callback: CallbackQuery):
#     tm = callback.data.split()
#     await callback.message.answer(f'Вы выбрали  {tm[1]}')
#     print(tm)
#     await callback.message.delete()
#
#
# # @router.message(Command('register'))
# # async def register(message: Message, state: FSMContext):
# #     await state.set_state(st.Register.name)
# #     await message.answer('Введите ваше имя')
#
# @router.message(F.text == 'Зарегистрируйтесь')
# async def register(message: Message, state: FSMContext):
#     await state.set_state(st.Register.name)
#     await message.answer('Введите ваше имя')
#
#
# @router.message(st.Register.name)
# async def register_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(st.Register.age)
#     await message.answer('Введите ваш возраст')
#
#
# @router.message(st.Register.age)
# async def register_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(st.Register.phone)
#     await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)
#
#
# @router.message(st.Register.phone, F.contact)
# async def register_phone(message: Message, state: FSMContext):
#     try:
#         await state.update_data(phone=message.contact.phone_number)
#         # phone=message.contact.phone_number
#         data = await state.get_data()
#         await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nНомер: {data["phone"]}',
#                              reply_markup=kb.main)
#     except KeyError:
#         # reply_markup=types.ReplyKeyboardRemove() - так можно удалить клавиатуру
#         print(data)
#         print(state.key)
#     await state.clear()
#
#     @router.message(F.text.contains('hgchgfghhghgfh'))
#     async def ggg(message: Message):
#         await message.answer('qqqq')
#
#
# # when user sends `/start` command, answering with inline calendar
# # @router.message(CommandStart())
# # async def command_start_handler(message: Message) -> None:
# #     """
# #     This handler receives messages with `/start` command
# #     """
# #     await message.reply(f"Hello, {hbold(message.from_user.full_name)}! Pick a calendar", reply_markup=kb.InlineKeyboardMarkupstart_kb)
#
#
# # default way of displaying a selector to user - date set for today
# @router.message(F.text.lower() == 'navigation calendar')
# async def nav_cal_handler(message: Message):
#     await message.answer(
#         "Please select a date: ",
#         reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
#     )
#
#
# # can be launched at specific year and month with allowed dates range
# @router.message(F.text.lower() == 'navigation calendar w month')
# async def nav_cal_handler_date(message: Message):
#     calendar = SimpleCalendar(
#         locale=await get_user_locale(message.from_user), show_alerts=True
#     )
#     calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
#     await message.answer(
#         "Calendar opened on feb 2023. Please select a date: ",
#         reply_markup=await calendar.start_calendar(year=2023, month=2)
#     )
#
#
# # simple calendar usage - filtering callbacks of calendar format
# @router.callback_query(SimpleCalendarCallback.filter())
# async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
#     calendar = SimpleCalendar(
#         locale=await get_user_locale(callback_query.from_user), show_alerts=True
#     )
#     calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
#     selected, date = await calendar.process_selection(callback_query, callback_data)
#     if selected:
#         await callback_query.message.answer(
#             f'You selected {date.strftime("%d/%m/%Y")}',
#             reply_markup=kb.start_kb
#         )
#     print(f'You selected {date.strftime("%d/%m/%Y")}')
#     # kb.create_keyboard_day()
#     await callback_query.message.answer('Выберите время', reply_markup=kb.kb_keybord_day)
#     await callback_query.message.delete()
#
#
# @router.message(F.text.lower() == 'dialog calendar')
# async def dialog_cal_handler(message: Message):
#     await message.answer(
#         "Please select a date: ",
#         reply_markup=await DialogCalendar(
#             locale=await get_user_locale(message.from_user)
#         ).start_calendar()
#     )
#
#
# # starting calendar with year 1989
# @router.message(F.text.lower() == 'dialog calendar w year')
# async def dialog_cal_handler_year(message: Message):
#     await message.answer(
#         "Calendar opened years selection around 1989. Please select a date: ",
#         reply_markup=await DialogCalendar(
#             locale=await get_user_locale(message.from_user)
#         ).start_calendar(1989)
#     )
#
#
# # starting dialog calendar with year 1989 & month
# @router.message(F.text.lower() == 'dialog calendar w month')
# async def dialog_cal_handler_month(message: Message):
#     await message.answer(
#         "Calendar opened on sep 1989. Please select a date: ",
#         reply_markup=await DialogCalendar(
#             locale=await get_user_locale(message.from_user)
#         ).start_calendar(year=1989, month=9)
#     )
#
#
# # dialog calendar usage
# @router.callback_query(DialogCalendarCallback.filter())
# async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
#     selected, date = await DialogCalendar(
#         locale=await get_user_locale(callback_query.from_user)
#     ).process_selection(callback_query, callback_data)
#     if selected:
#         await callback_query.message.answer(
#             f'You selected {date.strftime("%d/%m/%Y")}',
#             reply_markup=kb.start_kb
#         )
#
# # @router.message()
# # async def echo(message: Message):
# #     await message.send_copy(chat_id=message.from_user.id)

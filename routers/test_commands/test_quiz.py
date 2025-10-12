

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.poll import get_poll_result
from db.quiz import if_exists_quiz, get_quiz_title
from keyboards.keyboards import kb_quiz_push
from states.test import Test

router = Router(name=__name__)

@router.message(Command("test_quiz"))
async def test_quiz(message: Message, state: FSMContext):
    await state.set_state(Test.begin)
    await message.answer(f"введите ID квиза")

@router.message(F.text, Test.begin)
async def test_quiz(message: Message, state: FSMContext):
    if await if_exists_quiz(quiz_id=int(message.text)):
        await state.update_data(quiz_id=int(message.text))
        await message.answer("Такой квиз существует")
        quiz = await get_quiz_title(quiz_id=int(message.text))
        await message.answer(f"Название квиза {quiz.title}")
        await state.set_state(Test.push)
        await message.answer(f"Запускаем?", reply_markup=kb_quiz_push)
    else:
        await message.answer("Не  существует")



@router.message(Command('test'))
async def send_all(message: Message):
    result = await get_poll_result(poll_id=30)
    for i in result:
        # print(i["question"], i["count"], i["user_answer"])
        print(i[0], i[1], i[2],i[3])
        print(type(i))
        for a in i:
            print(a)



    # if not await if_user_end_quiz(quiz_id=96, user_id="878642217"):
    #     await message.answer(text="ТЕСТ НЕ БЫЛ ПРОЙДЕН")
    # else:
    #     await message.answer(text="ВЫ УЖЕ ПРОШЛИ ЭТОТ ТЕСТ")

    # res: dict = await get_quiz_result(quiz_id=97)
    # for k, v in res.items():
    #     print(f"key = {int(k)}: v = {int(v)}")
    # my_quiz = await bot.send_poll(chat_id=settings.TRINITY_GROUP_CHAT_ID, #7740157654,
    #                               question='Мессенджер, автор которого Павел Дуров',
    #                               options=['Telegram', 'Viber', 'WhatsApp', 'Messenger'],
    #                               type='quiz',
    #                               correct_option_id=0,
    #                               is_anonymous=False)
    # my_quiz2 = await bot.send_poll(chat_id=message.chat.id, question='Мессенджер, автор которого Павел Дуров', options=['Telegram', 'Viber', 'WhatsApp', 'Messenger'], type='quiz', correct_option_id=0, is_anonymous=False)
    #
    # my_quiz3 = await bot.send_poll(chat_id=709231639,
    #                                question='Какой термин описывает ситуацию, когда компании имитируют экологичность ради прибыли?',
    #                                options=['Карбоновый след', 'Гринвошинг', 'Устойчивый маркетинг', 'ESG-рейтинг'],
    #                                type='quiz',
    #                                correct_option_id=1,
    #                                is_anonymous=False)
    # await send_message_text_to_user_handler(text=f"Молодец, ты был первым, получи свою Звездочку {GLOWING_STAR}", uuid=709231639)

    # print(message.chat.id)
    # print(my_quiz.poll.correct_option_id)
    # print(my_quiz.poll.id)
    # # print(my_quiz2.poll.id)

# @router.poll_answer()
# async def handle_answer(answer: PollAnswer):
#     # await bot.send_message(chat_id=answer)
#     print('555555555555555555555555555555')
#     print(answer)


@router.message(Command('test1'))
async def send_all(message: Message):


    print(f"message.chat.id ---> {message.chat.id}")
    print(f"message.from_user.id --->{message.from_user.id}")
    print((message))
    # print(f" --->{message.from_user.}")



# @router.poll_answer()
# async def send_all(quiz_answer: PollAnswer):
#     await bot.send_message(quiz_answer.user.id, "YES")
#     print(quiz_answer.user.id)
#     print(quiz_answer.option_ids[0])
#     print(quiz_answer)
#     # await bot.send_message(chat_id="709231639", text="444444444444")
#     # await bot.send_message(chat_id="878642217", text="3333333333")
#     # uuids = await get_users_by_role(role=Roles.USER)
#     # print(len((uuids)))
#     # for uuid in uuids:
#     #     print(uuid)
#     # for i in range(1000):
#     #     await send_message_text_to_user_handler(uuid="878642217", text=str(i))


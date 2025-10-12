from aiogram import html

Q_AGE: str = "Сколько тебе лет?"
Q_GENDER: str = "Какой твой пол?"
A_ERROR_TRY_AGAIN: str = "Пожалуйста, сделай правильный выбор \U0001F446"
A_SECS_FEMALE: str = "Спасибо!!! \U0001F490"
A_SECS_MALE: str = "Спасибо!!! \U0000270C"
THINKING_FACE: str = "\U0001F914"
FOLDED_HANDS: str = "\U0001F64F"
POINTING_DOWN: str = "\U0001F447"
GLOWING_STAR: str = "\U0001F31F"
RED_QUESTION_MARK: str = "\U00002753"
A_CHOICE_PHOTO: str = (
    f"Выберите <b>{"фотографию"}</b> которую нужно добавить в рассылку.\n"
    f"<b>{"ИЛИ"}</b>\n"
    f"нажмите {html.bold("Далее")} если фотография не нужна\n"
    f"{html.bold("ИЛИ")}\n"
    f"{html.bold("Отмена")} для отказа от рассылки."
)
A_HELP_FOR_ADMIN: str = (
    f"Наберите на клавиатуре <b>{"/mailing"}</b> для создания рассылки пользователям.\n"
    f"Наберите на клавиатуре <b>{"/sendvideo"}</b> для создания видео рассылки пользователям.\n"
    f"Наберите на клавиатуре <b>{"/quizjson"}</b> для создания квиза на основе JSON файла.\n"
    f"<b>{"/poll"}</b> для отправки опроса.\n"
    f"{html.bold("ИЛИ")}\n"
    f"Наберите на клавиатуре <b>{"/menu"}</b> для для входа в интерактивное меню администратора.\n"
)

A_MENU_FOR_ADMIN: str = (
    f"Для отправки видео на сервер и получения video_id <b>{"/uploadvideo"}</b>. \n"
    f"Сделать пользователя АДМИНИСТРАТОРОМ <b>{"/createadmin"}</b>. \n"
    f"Просмотреть базу пользователей <b>{"/viewusers"}</b>. \n"

)

A_HELP_FOR_USER: str = (
    f"Описание что, зачем и почему.\n"
)

A_ERROR_MESSAGE_ANSVER: list = [
    "Ох, не знаю что ответить",
    "Не совсем понятно, что ты имеешь в виду",
    "Хмм...",
    RED_QUESTION_MARK
]


"""
Отправить квиз или конкретному пользователю - тогда указываем UUID
или None если всем пользователям
"""
SEND_QUIZ_ALL_OR_ONE = "7740157654"
# SEND_QUIZ_ALL_OR_ONE = None

BEGIN_VIDEO_ID_ANSWER: str = "BAACAgIAAxkBAAIkO2jTkDANpvxW1zoE06TrgYUFdQktAAJ0jAACnHSYSsBECWC5OFrFNgQ"

EMOJI_NUM = {"1": "1️⃣",
             "2": "2️⃣",
             "3": "3️⃣",
             "4": "4️⃣",
             "5": "5️⃣",
             "6": "6️⃣"
             }

EMOJI_ALL = {"star": "⭐",
             "envelope": "📩",
             "double": "‼️",
             "question": "⁉️",
             "cross_mark": "❎",
             "collision": "💥",
             "OK": "👌",
             "victory": "✌️",
             "tree": "🌲",
             "pepper": "🌶",
             "knopka": "📌",

}

PASSWORDS = {
    "admin": "12345678",
    "other": "87654321",
}
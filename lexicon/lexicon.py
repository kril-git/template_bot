LEXICON = {
    "/poll": f"Жду <i>JSON</i> файл опроса или /cancel для отмены действий:",
    "/cancel_poll": f"<i>Рассылка опроса отменена.</i>",
}

LEXICON_COMMANDS_ADMIN = {
    "/mailing": "<b>рассылки пользователям текста и фото.</b>",
    "/sendvideo": "<b>рассылка видео.</b>",
    "/quizjson": "<b>рассылка квиза из файла JSON.</b>",
    "/poll": "<b> рассылка опроса из файла JSON.</b>",
    "/menu": "<b>перейти в меню администратора.</b>",
}

POLL_ANSWER_TEXT = {
    "0": "ДА",
    "1": "НЕТ",
    "-1": "50/50",
}

LEXICON_COMMANDS_ADMIN_MENU = {
    "/uploadvideo": "для отправки видео на сервер и получения video_id",
    "/createadmi": "сделать пользователя АДМИНИСТРАТОРОМ",
    "/viewusers": "просмотреть базу пользователей",
    "/viewtablepoll": "посмотреть все опросы пользователей",
    "/getresultpoll": "получить результат опроса по его ID",
    "/getresultpolltail": "получить результат последних (пяти) опросов",
}

POLL_LIMIT: int = 5

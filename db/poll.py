import logging
from datetime import datetime
from typing import Any

from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import POLL_LIMIT
from models import Quiz, QuizOption, QuizAnswer, Poll, PollAnswer
from .crud import connection

logger = logging.getLogger(__name__)


@connection
async def create_poll(session: AsyncSession, data: dict, uuid: str) -> int:
    poll: Poll = Poll()
    poll.uuid = uuid
    poll.title = data.get("title")
    poll.type = data.get("type")
    poll.v = data.get("v")
    poll.question = data.get("question")
    poll.is_anonymous = data.get("is_anonymous")
    poll.date_start = datetime.strptime(data.get("date_start"), "%d-%m-%Y").date()
    poll.date_end = datetime.strptime(data.get("date_end"), "%d-%m-%Y").date()
    session.add(poll)
    try:
        await session.commit()
        return poll.id
    except Exception as e:
        logger.error(e)
        await session.rollback()
        return -1


# @connection
# async def get_all_quizid(session: AsyncSession) -> list[int]:
#     stmt = (
#         select(Quiz.id)
#     )
#     result = await session.execute(stmt)
#     answer: list = result.scalars().all()
#     return answer


# @connection
# async def get_quiz_answer_by_id(session: AsyncSession, quiz_id: int) -> list[QuizOption]:
#     stmt = (
#         select(QuizOption).where(QuizOption.quiz_id == quiz_id)
#     )
#     result = await session.execute(stmt)
#     answer: list = result.scalars().all()
#     return answer


# @connection
# async def get_quiz_correct_answer_by_id(session: AsyncSession, quiz_id: int) -> str:
#     stmt = (
#         select(QuizOption.answer).where(and_(QuizOption.quiz_id == quiz_id, QuizOption.correct_option_id == True))
#     )
#     result = await session.execute(stmt)
#     return result.scalar()


# @connection
# async def if_exists_quiz(session: AsyncSession, quiz_id: int) -> bool:
#     stmt = (
#         select(QuizOption).where(QuizOption.quiz_id == quiz_id)
#     )
#     result = await session.execute(stmt)
#     answer: list = result.scalars().all()
#     if len(answer) == 0:
#         return False
#     else:
#         return True


@connection
async def get_poll_title(session: AsyncSession, poll_id: int) -> Poll:
    stmt = (
        select(Poll).where(Poll.id == poll_id)
    )
    result = await session.execute(stmt)
    answer = result.scalars().one()
    return answer


# @connection
# async def get_quiz_correct_answer(session: AsyncSession, quiz_id: int) -> int:
#     stmt = (
#         select(QuizOption.option_id).where(
#             and_(QuizOption.quiz_id == quiz_id,
#                  QuizOption.correct_option_id == True)
#         )
#     )
#     result = await session.execute(stmt)
#     return result.scalar()


@connection
async def create_poll_answer(session: AsyncSession, data: dict) -> bool:
    poll_answer_entity: PollAnswer = PollAnswer()
    poll_answer_entity.poll_id = int(data['poll_id'])
    poll_answer_entity.user_id = str(data['user_id'])
    poll_answer_entity.user_answer = int(data['user_answer'])
    poll_answer_entity.poll_end = data['poll_end']
    session.add(poll_answer_entity)
    try:
        await session.commit()
        return True
    except Exception as e:
        logger.error(e)
        await session.rollback()
        return False


@connection
async def if_user_end_poll(session: AsyncSession, poll_id: int, user_id: str) -> bool:
    """
    Проверяем, пройден ли опрос пользователем
    """
    stmt = (
        select(PollAnswer.poll_end).where(
            and_(PollAnswer.poll_id == poll_id,
                 PollAnswer.user_id == user_id))
    )
    result = await session.execute(stmt)
    res = result.scalar_one_or_none()
    if res is None:
        return False
    else:
        return True


@connection
async def get_all_polls(session: AsyncSession) -> list[Poll]:
    stmt = select(Poll)
    poll = await session.scalars(stmt)
    return poll

@connection
async def get_all_polls_tail(session: AsyncSession) -> list[Poll]:
    stmt = select(Poll).order_by(desc(Poll.id)).limit(POLL_LIMIT)
    poll = await session.scalars(stmt)
    return poll


@connection
async def get_poll_result(session: AsyncSession, poll_id: int) -> Any:
    """
    select pollanswer.poll_id,  pollanswer.user_answer, count(pollanswer.user_answer) as con
    from pollanswer where poll_id = 25
    group by pollanswer.poll_id, pollanswer.user_answer

    select poll.question, pollanswer.poll_id,  pollanswer.user_answer, count(pollanswer.user_answer) as con
    from pollanswer
    inner join poll on poll.id = pollanswer.poll_id
    where poll_id = 25
    group by pollanswer.poll_id, pollanswer.user_answer, poll.question
    """
    stmt = (select(Poll.question, PollAnswer.poll_id, PollAnswer.user_answer, func.count(PollAnswer.user_answer).label("count"))
            .join(Poll, Poll.id == PollAnswer.poll_id)
            .where(PollAnswer.poll_id == poll_id)
            .group_by(PollAnswer.poll_id, PollAnswer.user_answer, Poll.question))
    result = await session.execute(stmt)
    return result

@connection
async def get_quiz_result(session: AsyncSession, quiz_id: int) -> dict:
    """
    Получаем словарь результатов квиза
    """

    stmt = select(
        QuizAnswer.user_answer,
        func.count(QuizAnswer.user_answer).label('count')
    ).group_by(
        QuizAnswer.user_answer
    )
    result = await session.execute(stmt)
    res = {}
    for item in result:
        res[str(item.user_answer)] = item.count
    return res

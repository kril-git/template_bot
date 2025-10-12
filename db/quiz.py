import logging
from datetime import datetime

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Quiz, QuizOption, QuizAnswer
from .crud import connection

logger = logging.getLogger(__name__)


@connection
async def create_quiz(session: AsyncSession, data: dict, uuid: str) -> int:
    quiz: Quiz = Quiz()
    quiz.uuid = uuid
    quiz.title = data.get("title")
    # quiz.description = data.get("type")
    quiz.type = data.get("type")
    quiz.v = data.get("v")
    quiz.question = data.get("question")
    quiz.correct_option_id = data.get("correct_option_id")
    quiz.is_anonymous = data.get("is_anonymous")
    quiz.password = data.get("password")
    quiz.date_start = datetime.strptime(data.get("date_start"), "%d-%m-%Y").date()
    quiz.date_end = datetime.strptime(data.get("date_end"), "%d-%m-%Y").date()
    session.add(quiz)
    try:
        await session.commit()
        options_list = data.get("options")
        count = 0
        for i in options_list:
            options: QuizOption = QuizOption()
            options.quiz_id = quiz.id
            options.option_id = count
            if count == quiz.correct_option_id:
                options.correct_option_id = True
            else:
                options.correct_option_id = False
            options.answer = i
            count = count + 1
            session.add(options)
        await session.commit()
        return quiz.id
    except Exception as e:
        logger.error(e)
        await session.rollback()
        return -1


@connection
async def get_all_quizid(session: AsyncSession) -> list[int]:
    stmt = (
        select(Quiz.id)
    )
    result = await session.execute(stmt)
    answer: list = result.scalars().all()
    return answer


@connection
async def get_quiz_answer_by_id(session: AsyncSession, quiz_id: int) -> list[QuizOption]:
    stmt = (
        select(QuizOption).where(QuizOption.quiz_id == quiz_id)
    )
    result = await session.execute(stmt)
    answer: list = result.scalars().all()
    return answer


@connection
async def get_quiz_correct_answer_by_id(session: AsyncSession, quiz_id: int) -> str:
    stmt = (
        select(QuizOption.answer).where(and_(QuizOption.quiz_id == quiz_id, QuizOption.correct_option_id == True))
    )
    result = await session.execute(stmt)
    return result.scalar()


@connection
async def if_exists_quiz(session: AsyncSession, quiz_id: int) -> bool:
    stmt = (
        select(QuizOption).where(QuizOption.quiz_id == quiz_id)
    )
    result = await session.execute(stmt)
    answer: list = result.scalars().all()
    if len(answer) == 0:
        return False
    else:
        return True


@connection
async def get_quiz_title(session: AsyncSession, quiz_id: int) -> Quiz:
    stmt = (
        select(Quiz).where(Quiz.id == quiz_id)
    )
    result = await session.execute(stmt)
    answer = result.scalars().one()
    return answer


@connection
async def get_quiz_correct_answer(session: AsyncSession, quiz_id: int) -> int:
    stmt = (
        select(QuizOption.option_id).where(
            and_(QuizOption.quiz_id == quiz_id,
                 QuizOption.correct_option_id == True)
        )
    )
    result = await session.execute(stmt)
    return result.scalar()


@connection
async def create_quiz_answer(session: AsyncSession, data: dict):
    quiz_answer_entity: QuizAnswer = QuizAnswer()
    print(data.items())
    quiz_answer_entity.quiz_id = data['quiz_id']
    quiz_answer_entity.user_id = str(data['user_id'])
    quiz_answer_entity.user_answer = data['user_answer']
    quiz_answer_entity.quiz_end = data['quiz_end']
    quiz_answer_entity.correct = data['yes']
    session.add(quiz_answer_entity)
    try:
        await session.commit()
    except Exception as e:
        logger.error(e)
        await session.rollback()


@connection
async def if_user_end_quiz(session: AsyncSession, quiz_id: int, user_id: str) -> bool:
    """
    Проверяем, пройден ли квиз пользователем
    """
    stmt = (
        select(QuizAnswer.quiz_end).where(
            and_(QuizAnswer.quiz_id == quiz_id,
                 QuizAnswer.user_id == user_id))
    )
    result = await session.execute(stmt)
    res = result.scalar_one_or_none()
    if res is None:
        return False
    else:
        return True


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

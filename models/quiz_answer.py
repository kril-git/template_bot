from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean
from sqlalchemy import Enum
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from models.base import Base
from utils.ERoles import Roles
from utils.EGender import Genders
import alembic_postgresql_enum

if TYPE_CHECKING:
    from .post import Post


class QuizAnswer(Base):
    __tablename__ = "quizanswer"

    """
    id: первичный ключ в таблице
    quiz_id: уникальный номер квиза (Integer)
    user_id: уникальный идентификатор пользователя String(100)
    user_answer: номер ответа который пользователь выбрал в квизе (Integer)
    quiz_end: прошел ли пользователь текущий квиз (Boolean)
    date_quiz: дата когда пользователь прошел квиз (DateTime)
    correct: правильно ли пользователь ответил в квизе (Boolean) 
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False)
    user_answer: Mapped[int] = mapped_column(Integer, nullable=False)
    quiz_end: Mapped[bool] = mapped_column(Boolean, default=False)
    date_quiz: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    correct: Mapped[bool] = mapped_column(Boolean, default=False)


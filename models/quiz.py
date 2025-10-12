from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from models.base import Base

if TYPE_CHECKING:
    from .post import Post


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(100), unique=False)
    title: Mapped[str] = mapped_column(String(150), unique=False, nullable=True)
    type: Mapped[str] = mapped_column(String(10), unique=False, nullable=True, default="quiz")
    v: Mapped[int] = mapped_column(Integer, default=1, nullable=True)
    question: Mapped[str] = mapped_column(String(300), unique=False, nullable=True)
    correct_option_id: Mapped[int] = mapped_column(Integer, nullable=True)
    date_create: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=True)
    date_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    date_end: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    options: Mapped[list["QuizOption"]] = relationship(back_populates="quiz")

    # def __str__(self) -> str:
    #     return f"{self.__class__.__name__}(id={self.id}, uuid={self.uuid!r}, role={self.role!r})"

    # def __repr__(self) -> str:
    #     return str(self)


class QuizOption(Base):
    __tablename__ = "quiz_options"
    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    option_id: Mapped[int] = mapped_column(Integer, nullable=True)
    correct_option_id: Mapped[int] = mapped_column(Boolean, default=False)
    answer: Mapped[str] = mapped_column(String(150), nullable=True)
    quiz: Mapped["Quiz"] = relationship(back_populates="options")

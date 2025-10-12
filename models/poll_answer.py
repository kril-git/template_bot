from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy import Enum
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from models.base import Base





class PollAnswer(Base):
    __tablename__ = "pollanswer"

    """
    id: первичный ключ в таблице
    poll_id: уникальный номер опроса (Integer)
    user_id: уникальный идентификатор пользователя String(100)
    user_answer:  0 - да,
                  1 - нет,
                 -1 - затрудняюсь ответить(Integer)
    poll_end: прошел ли пользователь текущий опрос (Boolean)
    date_poll: дата когда пользователь прошел опрос (DateTime)
    correct: правильно ли пользователь ответил в опросе (Boolean) 
    
        # poll_id: Mapped[int] = mapped_column(ForeignKey("poll.id"))

    """

    id: Mapped[int] = mapped_column(primary_key=True)
    poll_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False)
    user_answer: Mapped[int] = mapped_column(Integer, nullable=False)
    poll_end: Mapped[bool] = mapped_column(Boolean, default=False)
    date_poll: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )



from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from models.base import Base


class Poll(Base):
    __tablename__ = "poll"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(100), unique=False)
    title: Mapped[str] = mapped_column(String(150), unique=False, nullable=True)
    type: Mapped[str] = mapped_column(String(10), unique=False, nullable=True, default="poll")
    v: Mapped[int] = mapped_column(Integer, default=1, nullable=True)
    question: Mapped[str] = mapped_column(String(300), unique=False, nullable=True)
    answer: Mapped[int] = mapped_column(Integer, nullable=True)
    date_create: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=True)
    date_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    date_end: Mapped[DateTime] = mapped_column(DateTime(timezone=True))


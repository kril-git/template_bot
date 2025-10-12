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


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(100), unique=True)
    role: Mapped[Roles] = mapped_column(Enum(Roles), default=Roles.USER)
    first_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
    user_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
    nic_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    registration: Mapped[bool] = mapped_column(Boolean, default=False)
    gender: Mapped[Genders] = mapped_column(Enum(Genders), nullable=True)
    date_create: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_update: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_visit: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now()
    )

    posts: Mapped[list["Post"]] = relationship(back_populates="users")

    # def __str__(self) -> str:
    #     return f"{self.__class__.__name__}(id={self.id}, uuid={self.uuid!r}, role={self.role!r})"

    # def __repr__(self) -> str:
    #     return str(self)

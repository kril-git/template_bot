from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from models.base import Base
from .mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_unic = True
    _user_id_nullable = False
    _user_back_populates = "profile"

    _nic_name_default: str = "NoName"
    _phone_number_default: str = "+000-00-0000000"
    _str_default: str = ""

    profile_default: dict = {
        "nic_name": _nic_name_default,
        "phone_number": _phone_number_default,
        "first_name": _str_default,
        "last_name": _str_default,
        "email": _str_default,
        "age": 0,
    }

    __tablename__ = "profile"
    # id: Mapped[int] = mapped_column(primary_key=True)
    nic_name: Mapped[str] = mapped_column(String(30), unique=True, default="NoName")
    first_name: Mapped[str | None] = mapped_column(String(30), unique=False)
    last_name: Mapped[str | None] = mapped_column(String(30), unique=False)
    email: Mapped[str | None] = mapped_column(String(256), unique=True)
    phone_number: Mapped[str] = mapped_column(
        String(50), unique=True, default="+000-00-0000000"
    )
    age: Mapped[int | None] = mapped_column(Integer)
    date_create: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_update: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)

    # def __str__(self) -> str:
    #     return f"User(id = {self.id!r}, name = {self.nic_name!r})"

    # def __repr__(self) -> str:
    #     # return super().__repr__()
    #     return str(self)

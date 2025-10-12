from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .user import User


class Post(UserRelationMixin, Base):
    _user_id_nullable = False
    _user_id_unic = False
    _user_back_populates = "posts"

    __tablename__ = "posts"
    # id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    # переделали используя класс mixins
    # # Make database tables link
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    #
    # # Make connection between models
    # user: Mapped["User"] = relationship(back_populates="posts")

    def __str__(self) -> str:
        return f"Post(id = {self.id!r}, title = {self.title!r})"

    def __repr__(self) -> str:
        # return super().__repr__()
        return str(self)

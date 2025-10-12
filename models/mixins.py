from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

if TYPE_CHECKING:
    from .user import User


class UserRelationMixin:
    _user_id_unic: bool = False
    _user_id_nullable: bool = False
    _user_back_populates: str | None = None

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id"),
            unique=cls._user_id_unic,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def users(cls) -> Mapped["User"]:
        return relationship("User", back_populates=cls._user_back_populates)

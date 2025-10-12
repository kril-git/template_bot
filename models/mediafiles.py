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


class MediaContent(Base):
    __tablename__ = "mediacontent"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[str] = mapped_column(String(100), unique=True)
    file_caption: Mapped[str] = mapped_column(String(100), default=None)
    file_type: Mapped[str] = mapped_column(String(2), default=None)
    file_name: Mapped[str] = mapped_column(String(50), default=None)
    uuid_user_upload: Mapped[str] = mapped_column(String(100), unique=False)
    date_create: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_send: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


import logging

from sqlalchemy import select, Result, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.crud import connection
from models import MediaContent
from utils import ERoles
from utils.db_helper import db_helper
# from utils.common import connection
from models.user import User
from datetime import datetime
from utils.ERoles import Roles

logger = logging.getLogger(__name__)


@connection
async def create_new_mediacontent(session: AsyncSession, mediacontent: MediaContent) -> MediaContent:
    session.add(mediacontent)
    await session.commit()
    return mediacontent


# @connection
# async def if_exist_user_by_uuid(session: AsyncSession, uuid: str) -> bool:
#     stmt = select(User).where(User.uuid == uuid)
#     result: Result = await session.execute(stmt)
#     uses: User | None = result.scalar_one_or_none()
#     if uses is None:
#         return False
#     else:
#         return True
#
#
# @connection
# async def get_user_by_uuid(session: AsyncSession, uuid: str) -> User:
#     stmt = select(User).where(User.uuid == uuid)
#     result: Result = await session.execute(stmt)
#     user: User = result.scalar()
#     return user



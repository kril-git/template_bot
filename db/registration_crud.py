import logging
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud import get_user_by_uuid, connection

logger = logging.getLogger(__name__)


@connection
async def update_reg_info_user(session: AsyncSession, data: dict):
    user = await get_user_by_uuid(uuid=str(data.get("uuid")))
    user.nic_name = data.get("name")
    user.age = data.get("age")
    user.gender = data.get("gender")
    user.registration = True
    session.add(user)
    await session.commit()

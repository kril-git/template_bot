import logging
from db.crud import update_role_user_to_admin, get_users_by_role

logger = logging.getLogger(__name__)


async def update_role_to_admin(user_id: int | list[int]) -> int:
    count: int = 0
    if isinstance(user_id, int):
        await update_role_user_to_admin(id_user=user_id)
        return count + 1
    if isinstance(user_id, list):
        for id_user in user_id:
            await update_role_user_to_admin(id_user=id_user)
            count = count + 1
        return count


async def get_list_uuid_admins() -> list[str]:
    list_uuid_admins: list[str] = await get_users_by_role()
    return list_uuid_admins

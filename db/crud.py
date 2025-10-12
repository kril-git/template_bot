import logging

from sqlalchemy import select, Result, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from utils import ERoles
from utils.db_helper import db_helper
# from utils.common import connection
from models.user import User
from datetime import datetime
from utils.ERoles import Roles

logger = logging.getLogger(__name__)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with db_helper.session_factory() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                logger.error(e)
                raise e
            finally:
                await session.close()

    return wrapper


@connection
async def if_exist_user_by_uuid(session: AsyncSession, uuid: str) -> bool:
    stmt = select(User).where(User.uuid == uuid)
    result: Result = await session.execute(stmt)
    uses: User | None = result.scalar_one_or_none()
    if uses is None:
        return False
    else:
        return True


@connection
async def get_user_by_uuid(session: AsyncSession, uuid: str) -> User:
    stmt = select(User).where(User.uuid == uuid)
    result: Result = await session.execute(stmt)
    user: User = result.scalar()
    return user


@connection
async def create_new_user(session: AsyncSession, user: User) -> User:
    session.add(user)
    await session.commit()
    return user


@connection
async def update_last_visit_user_by_id(session: AsyncSession, user: User) -> bool:
    stmt = (
        update(User).where(User.id == user.id).values(user_name=None, last_visit=datetime.now())
    )
    await session.execute(stmt)
    await session.commit()
    return True

@connection
async def create_admin(session: AsyncSession, user_uuid: str) -> User:
    stmt = (
        update(User).where(User.uuid == user_uuid).values(role=Roles.ADMIN)
    )
    await session.execute(stmt)
    await session.commit()
    user = await get_user_by_uuid(uuid=user_uuid)
    return user


@connection
async def if_exist_user(
        session: AsyncSession, entity: object, item: str
) -> bool | None:
    return True


@connection
async def get_users_by_role(session: AsyncSession, role: Roles = Roles.ADMIN) -> list[str]:
    stmt = (
        select(User.uuid).where(User.role == role)
    )
    result = await session.execute(stmt)
    uuids: list = result.scalars().all()
    return uuids


@connection
async def update_role_user_to_admin(session: AsyncSession, id_user: int) -> object:
    stmt = (
        update(User).where(User.id == id_user).values(role=Roles.ADMIN)
    )
    await session.execute(stmt)
    await session.commit()


# @connection
# async def create_user(
#     session: AsyncSession, uuid: str | None, dic_profile: dict | None
# ) -> User:
#
#     if uuid is None:
#         uuid = User(uuid=str(datetime.now().timestamp()))
#     else:
#         uuid = str(datetime.now().timestamp())
#     user = User(uuid=uuid)
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)
#     # profile = get_profile_by_dict(dict_profile=dic_profile, user_id=user.id)
#     session.add(profile)
#     await session.commit()
#     return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    # user: User | None = session.scalar(stmt) // тоже самое только одной строчкой
    return user


async def get_user_all(session: AsyncSession) -> list[User]:
    stmt = select(User)
    result: Result = await session.execute(stmt)
    users = await session.scalars(stmt)
    users1 = users.all()
    for user in users1:
        print(user.id, user.role)

    return users1


@connection
async def get_all_user_wrapper(session: AsyncSession) -> list[User]:
    stmt = select(User)
    users = await session.scalars(stmt)
    return users


@connection
async def get_all_users_fype_result(session: AsyncSession) -> Result:
    return await session.execute(select(User))


# @connection
# async def get_users_and_profile(session: AsyncSession) -> list:
#     stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
#     # result: Result = await session.execute(stmt)
#     # users = result.scalars()
#     users = await session.scalars(stmt)
#     for user in users:
#         print("user   ===> ", user)
#         if user.profile.last_name is not None:
#             print("user profile ==== >>> ", user.profile.last_name)
#     return users


@connection
# async def create_user_profile(session: AsyncSession, user_id: int) -> Profile:
#     profile = Profile(
#         nic_name="kril 7",
#         first_name="Dzmitry 7",
#         last_name="Krylovich 7",
#         email="sampasabe7@gmail.com",
#         phone_number="76261405",
#         user_id=user_id,
#     )
#     session.add(profile)
#     await session.commit()
#     return profile
#

async def main():
    pass
    # async with db_helper.session_factory() as session:
    # user = await create_user(session=session)
    #     # await get_user_by_id(session, user.id)
    #     # await create_user_profile(session, 1)
    #     users = await get_user_all(session)
    #     print(type(users))
    #     print(len(users))
    #     for user in users:
    #         print(user)
    #     AsyncSession.close
    #
    # await create_user(uuid=str(datetime.now().timestamp()), dic_profile=None)
    # profile = Profile(ModelsSettings.PROFILE_DEFAULT)
    # profile = Profile
    # print(Profile.__dict__)
    # for i in Profile.__dict__:
    #
    #     print(i)
    # for k, v in ModelsSettings.PROFILE_DEFAULT.items():
    #     setattr(profile, k, v)
    # # p = Profile(*attr)
    # print(profile.nic_name)
    #     # profile.nic_name = ModelsSettings.PROFILE_DEFAULT.values(i)
    #     getattr(profile, str(i))
    #     print(i)
    # # profile["user_id"] = 44
    # print(profile)

    # await create_user_profile(user_id=7)
    # users = await get_users_and_profile()

# for user in users:
#     print(user.profile.last_name)

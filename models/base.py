from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncAttrs
from config.app_settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    # pool_size=settings.ALCHEMY_POOL_SIZE,
    # max_overflow=settings.ALCHEMY_MAX_OVERFLOW
)

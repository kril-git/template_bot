from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.app_settings import settings


class DatabaseHelper:
    def __init__(self):
        self.engine = create_async_engine(
            url=settings.DATABASE_URL, echo=settings.DB_ECHO
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )


db_helper = DatabaseHelper()

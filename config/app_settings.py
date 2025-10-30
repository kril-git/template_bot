from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_TYPE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_ECHO: bool
    ALCHEMY_ECHO: bool
    ALCHEMY_POOL_SIZE: int
    ALCHEMY_MAX_OVERFLOW: int
    BOT_TOKEN: str
    BOT_NAME: str
    DEBUG_FILE_SETTINGS: str
    APP_DEBUG: bool
    FORMAT_LOGGING: str
    TIME_FORMAT_LOGGING: str
    ADMINS: list[str]
    COMMAND_MENU: dict[str, str]
    SEND_MAILING_ALL: bool
    TRINITY_GROUP_CHAT_ID: str
    PATH_FOR_QUIZ_FILES: str
    PATH_FOR_ALL_MEDIA_FILES: str = ""

    @property
    def DATABASE_URL(self):
        # DSN
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"{self.DB_TYPE}+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # case_sensitive=True -> должен совпадать регистр букв
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()

import logging
import os
from pathlib import Path

import coloredlogs
import yaml

from config.app_settings import settings
from services.services_admin import logger


def print_if_option_debug(message: str):
    if settings.APP_DEBUG:
        print(message)


def set_base_config_loaders_as_default(default_level=logging.INFO):
    custom_time_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(filename="logs/app.log", level=default_level, format=settings.FORMAT_LOGGING,
                        datefmt=settings.TIME_FORMAT_LOGGING)
    coloredlogs.install(level=default_level)


def setup_logging(env_key="LOG_CFG"):

    """
    Настройка логирования из YAML файла
    """

    path = os.getenv(env_key,
                     settings.DEBUG_FILE_SETTINGS)  # возвращает значение ключа key переменной среды, если оно
    # существует или значение по умолчанию default, если его нет.
    print_if_option_debug(f"Используем файл конфигурации {settings.DEBUG_FILE_SETTINGS}")
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config) # Применяем конфигурацию
                logger.info(f"Success Logging Configuration. Using {path}")
            except Exception as e:
                set_base_config_loaders_as_default()
                logger.error(f"Error in Logging Configuration. Using default configs. Path {path} not found. "
                             f"Exception -> {e}")

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True) # Создаем директорию для логов если ее нет
    else:
        set_base_config_loaders_as_default()
        logger.error("Error in Logging Configuration. Using default configs ")

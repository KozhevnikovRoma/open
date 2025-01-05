# automation/automation_config.py
import logging
from config.logging_config import LOGGING_CONFIG
import logging.config

# Настройка логирования
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Пример конфигурации для автоматизации
AUTOMATION_CONFIG = {
    "default_interval": "hourly",
    "notification_enabled": True
}

# Логируем настройки автоматизации
logger.info("Конфигурация автоматизации загружена успешно.")
logger.debug(f"Загруженные настройки автоматизации: {AUTOMATION_CONFIG}")

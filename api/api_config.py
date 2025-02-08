# api/api_config.py
import logging
from config.logging_config import LOGGING_CONFIG
import logging.config

# Настройка логирования
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Версия API
API_VERSION = "1.0"

# Конфигурация API
API_CONFIG = {
    "title": "AI Coordinator API",
    "version": "1.0.0",
    "description": "API for managing users, data, and logs within the AI Coordinator system.",
    "default_route_prefix": "/api",
    "allowed_file_types": ["json", "csv", "xlsx"]
}

# Логируем события
logger.info("API конфигурация загружена успешно.")
logger.debug(f"Загруженные настройки API: {API_CONFIG}")

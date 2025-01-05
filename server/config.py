# server/config.py
import os
from dotenv import load_dotenv
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Загрузка переменных окружения из файла .env
try:
    load_dotenv()
    logger.info("Переменные окружения успешно загружены из .env файла.")
except Exception as e:
    logger.warning(f"Ошибка при загрузке переменных окружения: {e}")

class Config:
    """Конфигурация для проекта."""
    
    def __init__(self):
        # Настройки сервера
        self.SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
        self.SERVER_PORT = self._get_int_env("SERVER_PORT", 8000)
        logger.info(f"Настройки сервера: HOST={self.SERVER_HOST}, PORT={self.SERVER_PORT}")
        
        # Настройки базы данных
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ai_coordinator.db")
        if not self.DATABASE_URL:
            logger.warning("DATABASE_URL не задан, используется значение по умолчанию.")
        logger.info(f"URL базы данных: {self.DATABASE_URL}")

        # Настройки AI-интерфейса
        self.AI_MODEL_PATH = os.getenv("AI_MODEL_PATH", "models/ai_model.bin")
        self.AI_API_KEY = os.getenv("AI_API_KEY", "your_api_key")
        logger.info(f"Путь к модели AI: {self.AI_MODEL_PATH}")
        if self.AI_API_KEY == "your_api_key":
            logger.warning("Используется ключ API по умолчанию. Проверьте настройки.")
    
    def _get_int_env(self, key: str, default: int) -> int:
        """Получить целочисленное значение из переменной окружения с обработкой ошибок."""
        try:
            return int(os.getenv(key, default))
        except ValueError:
            logger.warning(f"Некорректное значение для {key}, установлено значение по умолчанию {default}")
            return default

# Пример использования
config = Config()

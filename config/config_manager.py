import logging
from logging.handlers import RotatingFileHandler
from config.logging_config import LOGGING_CONFIG
import logging.config
import json
import os

class Config:
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8000

    @staticmethod
    def load_openai_config(file_path="config/openai_config.json"):
        """
        Load OpenAI API configuration from a JSON file.

        :param file_path: Path to the OpenAI configuration JSON file.
        :return: A dictionary containing OpenAI configuration values.
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
            with open(file_path, 'r') as file:
                config = json.load(file)
                required_keys = ["openai_api_key", "openai_base_url"]
                missing_keys = [key for key in required_keys if key not in config]
                
                if missing_keys:
                    raise ValueError(f"Missing required keys in OpenAI configuration: {missing_keys}")
                
                return config
        except Exception as e:
            logging.error(f"Error loading OpenAI configuration: {e}")
            return {}

class LogConfig:
    @staticmethod
    def setup_logger(name, log_file, level=logging.INFO):
        """
        Set up a logger with a rotating file handler.

        :param name: Name of the logger.
        :param log_file: File to store logs.
        :param level: Logging level.
        :return: Configured logger.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Create file handler with rotation
        handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Avoid duplicate handlers
        if not logger.handlers:
            logger.addHandler(handler)

        return logger

# Настройка глобального логирования с использованием конфигурации
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Пример использования логгера
logger.info("ConfigManager загружен и настроен.")

# Загрузка конфигурации OpenAI
openai_config = Config.load_openai_config()
if openai_config:
    logger.info("OpenAI конфигурация загружена успешно.")
else:
    logger.error("Не удалось загрузить конфигурацию OpenAI.")

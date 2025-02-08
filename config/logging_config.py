import logging
import logging.config
import os

# Путь для хранения логов
LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/app_logs.log")

# Конфигурация логирования
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH,
            'formatter': 'default',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'openai_api': {
            'level': 'DEBUG',
            'handlers': ['file', 'console'],
            'propagate': False,
        },
        'root': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    },
}

# Настройка глобального логирования для проекта
def setup_logging():
    """Настройка глобального логирования для проекта."""
    if not os.path.exists(os.path.dirname(LOG_PATH)):
        os.makedirs(os.path.dirname(LOG_PATH))

    logging.config.dictConfig(LOGGING_CONFIG)

# Вызов настройки логирования
setup_logging()

# Пример использования логирования в проекте
logger = logging.getLogger(__name__)

# Для OpenAI можно также использовать отдельный логгер:
openai_logger = logging.getLogger('openai_api')

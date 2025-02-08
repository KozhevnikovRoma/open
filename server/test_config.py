import os

class TestConfig:
    """Конфигурация для тестового режима."""
    TEST_MODE = True
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8001  # Порт для тестового режима
    DATABASE_URL = "sqlite:///test_ai_coordinator.db"  # Тестовая база данных
    MEMORY_STORAGE_PATH = os.path.join(os.path.dirname(__file__), "test_memory_storage.json")
    LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/test_logs.log")

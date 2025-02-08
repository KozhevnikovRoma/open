import pytest
import os
import sys

# Добавляем путь проекта в sys.path для импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../server")))

from test_config import TestConfig  # Импортируем тестовую конфигурацию

@pytest.fixture(scope="session")
def test_config():
    """Фикстура для предоставления тестовой конфигурации."""
    return TestConfig()

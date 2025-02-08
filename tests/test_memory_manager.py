import pytest
import os
import json
from memory.memory_manager import MemoryManager

# Тестовые данные
TEST_MEMORY_PATH = "test_memory_storage.json"

@pytest.fixture(scope="function", autouse=True)
def setup_memory_manager():
    """Фикстура для создания и удаления тестового хранилища памяти."""
    manager = MemoryManager()
    manager.memory = {}  # Обнуляем память
    manager._save_memory = lambda: None  # Отключаем запись в файл
    yield manager
    # Удаление тестового файла после тестов
    if os.path.exists(TEST_MEMORY_PATH):
        os.remove(TEST_MEMORY_PATH)

def test_set_and_get_memory(setup_memory_manager):
    """Тест: запись и чтение данных в память."""
    manager = setup_memory_manager
    key, value = "test_key", {"data": "test_value"}
    manager.set_memory(key, value)
    assert manager.get_memory(key) == value

def test_delete_memory(setup_memory_manager):
    """Тест: удаление данных из памяти."""
    manager = setup_memory_manager
    key, value = "test_key", "test_value"
    manager.set_memory(key, value)
    assert manager.get_memory(key) == value

    manager.delete_memory(key)
    assert manager.get_memory(key) is None

def test_get_nonexistent_memory(setup_memory_manager):
    """Тест: попытка чтения несуществующего ключа."""
    manager = setup_memory_manager
    assert manager.get_memory("nonexistent_key") is None

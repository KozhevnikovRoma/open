import json
import os
import logging
from threading import Lock
from typing import Any, Dict, Optional, List
import asyncio
from datetime import datetime

# Настройка пути и логирования
DEFAULT_MEMORY_STORAGE_PATH = os.path.join(os.path.dirname(__file__), "memory_storage.json")
LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/memory_logs.log")

# Настройка логгера
logger = logging.getLogger("memory_manager")
logger.setLevel(logging.INFO)

# Создаем обработчик для записи в файл
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(file_handler)


class MemoryManager:
    """Класс для управления памятью проекта с логированием и потокобезопасностью."""

    def __init__(self, storage_file: str = DEFAULT_MEMORY_STORAGE_PATH):
        """
        Инициализация класса MemoryManager.
        
        :param storage_file: Путь к файлу хранения памяти.
        """
        self.storage_file = storage_file
        self.memory = self._load_memory()
        self.lock = Lock()

    def _load_memory(self) -> Dict[str, Any]:
        """Загружает данные памяти из файла."""
        logger.info("Загрузка памяти из файла...")
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as file:
                    memory_data = json.load(file)
                logger.info("Память успешно загружена из файла.")
                return memory_data
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка декодирования памяти: {e}. Используется пустая память.")
            except Exception as e:
                logger.error(f"Ошибка при загрузке данных из файла памяти: {e}")
        else:
            logger.warning(f"Файл памяти '{self.storage_file}' не найден. Создана новая память.")
        return {}

    def _save_memory(self) -> None:
        """Сохраняет данные памяти в файл."""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as file:
                json.dump(self.memory, file, ensure_ascii=False, indent=4)
            logger.info(f"Память успешно сохранена в файл '{self.storage_file}'.")
        except Exception as e:
            logger.error(f"Ошибка сохранения памяти: {e}")

    def save_message(self, sender: str, message: str) -> None:
        """
        Сохраняет сообщение в историю общения.
        
        :param sender: Отправитель сообщения ("user" или "assistant").
        :param message: Текст сообщения.
        """
        logger.info(f"Сохранение сообщения от '{sender}'...")
        with self.lock:
            if "conversation" not in self.memory:
                self.memory["conversation"] = []
            self.memory["conversation"].append({
                "timestamp": datetime.now().isoformat(),
                "sender": sender,
                "message": message
            })
            self._save_memory()
        logger.info("Сообщение успешно сохранено.")

    def get_conversation(self) -> List[Dict[str, str]]:
        """
        Извлекает историю общения.
        
        :return: Список сообщений.
        """
        return self.memory.get("conversation", [])

    def get_memory(self, key: str) -> Optional[Any]:
        """Извлекает данные из памяти по ключу."""
        return self.memory.get(key)

    def set_memory(self, key: str, value: Any) -> None:
        """Сохраняет данные в память по ключу."""
        with self.lock:
            self.memory[key] = value
            self._save_memory()

    def delete_memory(self, key: str) -> None:
        """Удаляет данные из памяти по ключу."""
        with self.lock:
            if key in self.memory:
                del self.memory[key]
                self._save_memory()


# Экземпляр менеджера памяти
memory_manager = MemoryManager()

if __name__ == "__main__":
    # Пример использования
    memory_manager.save_message("user", "Привет, Лю!")
    memory_manager.save_message("assistant", "Привет, как я могу помочь?")
    print(memory_manager.get_conversation())

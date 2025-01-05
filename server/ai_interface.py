import json
import os
import logging
from memory.memory_manager import MemoryManager
from database.database_manager import DatabaseManager
from tools.performance_analyzer import PerformanceAnalyzer
from tools.cleanup_tool import CleanupTool
from tools.backup_manager import BackupManager

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщения
    handlers=[
        logging.StreamHandler(),  # Логирование в консоль
        logging.FileHandler("app.log")  # Логирование в файл app.log
    ]
)

# Получаем логгер
logger = logging.getLogger(__name__)

class AIInterface:
    """Класс интерфейса для взаимодействия с ИИ."""

    def __init__(self):
        self.memory_manager = MemoryManager()
        self.database_manager = DatabaseManager()
        self.performance_analyzer = PerformanceAnalyzer()
        self.cleanup_tool = CleanupTool()
        self.backup_manager = BackupManager()

    async def handle_request(self, request_type, params):
        """Центральный метод для обработки запросов ИИ и маршрутизации их к соответствующим компонентам."""
        logger.debug(f"Received request: {request_type} with params: {params}")
        try:
            if request_type == "memory":
                return await self._handle_memory_request(params)
            elif request_type == "database":
                return await self._handle_database_request(params)
            elif request_type == "performance":
                return await self._analyze_performance(params)
            elif request_type == "cleanup":
                return await self._cleanup_data(params)
            elif request_type == "backup":
                return await self._create_backup(params)
            else:
                logger.error(f"Unknown request type: {request_type}")
                return {"error": "Unknown request type"}
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return {"error": f"An unexpected error occurred: {str(e)}"}

    async def _handle_memory_request(self, params):
        """Обработка запросов, связанных с памятью."""
        logger.debug(f"Handling memory request with params: {params}")
        if "action" not in params:
            logger.warning("Action not specified in memory request.")
            return {"error": "Action not specified"}

        action = params["action"]

        if action == "read":
            key = params.get("key")
            if not key:
                logger.warning("Key is required for read action.")
                return {"error": "Key is required for read action"}
            value = self.memory_manager.get_memory(key)
            if value is None:
                logger.warning(f"Key '{key}' not found in memory.")
                return {"error": f"Key '{key}' not found in memory"}
            return {"data": value}
        elif action == "write":
            key, value = params.get("key"), params.get("value")
            if not key or value is None:
                logger.warning("Key and value are required for write action.")
                return {"error": "Key and value are required for write action"}
            await self.memory_manager.write_memory(key, value)
            logger.info(f"Data for key '{key}' written successfully.")
            return {"status": "success"}
        else:
            logger.error(f"Unknown memory action: {action}")
            return {"error": "Unknown memory action"}

    async def _handle_database_request(self, params):
        """Обработка запросов к базе данных."""
        query = params.get("query")
        if not query:
            logger.warning("Query not specified for database request.")
            return {"error": "Query not specified"}
        try:
            result = self.database_manager.execute_query(query)
            logger.info(f"Database query executed successfully: {query}")
            return {"data": result}
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            return {"error": f"Database error: {str(e)}"}

    async def _analyze_performance(self, params):
        """Анализ производительности системы."""
        logger.debug(f"Analyzing performance with params: {params}")
        return self.performance_analyzer.analyze(params)

    async def _cleanup_data(self, params):
        """Очистка данных."""
        target = params.get("target")
        if not target:
            logger.warning("Target not specified for cleanup.")
            return {"error": "Target not specified for cleanup"}
        self.cleanup_tool.cleanup(target)
        logger.info(f"Data cleanup performed for target: {target}")
        return {"status": "success"}

    async def _create_backup(self, params):
        """Создание резервной копии."""
        path = params.get("path")
        if not path:
            logger.warning("Path not specified for backup.")
            return {"error": "Path not specified for backup"}
        self.backup_manager.create_backup(path)
        logger.info(f"Backup created at path: {path}")
        return {"status": "success"}

# Режим самостоятельного выполнения для отладки
if __name__ == "__main__":
    ai = AIInterface()
    sample_request = {
        "request_type": "memory", 
        "params": {"action": "write", "key": "test", "value": {"example": "data"}}
    }
    result = ai.handle_request(sample_request["request_type"], sample_request["params"])
    logger.info(f"Request result: {result}")

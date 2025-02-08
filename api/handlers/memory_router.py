import logging
from fastapi import APIRouter, HTTPException
from memory.memory_manager import MemoryManager
from config.logging_config import LOGGING_CONFIG
import logging.config

# Настройка логирования
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

router = APIRouter()

# Инициализация менеджера памяти
memory_manager = MemoryManager()

@router.post("/memory/save/")
def save_memory(key: str, value: str):
    """Сохранение данных в память"""
    try:
        logger.debug(f"Запрос на сохранение данных: ключ = {key}, значение = {value}")
        memory_manager.set_memory(key, value)
        logger.info(f"Данные успешно сохранены по ключу: {key}")
        return {"message": "Data saved to memory successfully", "key": key, "value": value}
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных в память: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/{key}")
def get_memory(key: str):
    """Получение данных из памяти"""
    try:
        logger.debug(f"Запрос на получение данных по ключу: {key}")
        value = memory_manager.get_memory(key)
        if not value:
            logger.warning(f"Ключ не найден в памяти: {key}")
            raise HTTPException(status_code=404, detail="Key not found in memory")
        logger.info(f"Данные успешно извлечены по ключу: {key}")
        return {"key": key, "value": value}
    except Exception as e:
        logger.error(f"Ошибка при извлечении данных из памяти: {e}")
        raise HTTPException(status_code=500, detail=str(e))

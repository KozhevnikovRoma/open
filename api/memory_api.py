from fastapi import APIRouter, HTTPException
from memory.memory_manager import memory_manager

router = APIRouter()

@router.get("/memory/{key}")
async def get_memory(key: str):
    """Получение данных по ключу"""
    data = memory_manager.get_memory(key)
    if data is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "data": data}

@router.post("/memory/{key}")
async def set_memory(key: str, value: dict):
    """Сохранение данных по ключу"""
    memory_manager.set_memory(key, value)
    return {"message": "Data saved successfully", "key": key}

@router.delete("/memory/{key}")
async def delete_memory(key: str):
    """Удаление данных по ключу"""
    memory_manager.delete_memory(key)
    return {"message": "Data deleted successfully", "key": key}

from fastapi import APIRouter, HTTPException
from memory.memory_manager import memory_manager
from tools.openai_api import generate_text

router = APIRouter()

# Маршрут для получения данных из памяти по ключу
@router.get("/memory/{key}")
async def get_memory(key: str):
    """Получение данных по ключу"""
    data = memory_manager.get_memory(key)
    if data is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "data": data}

# Маршрут для сохранения данных в память по ключу
@router.post("/memory/{key}")
async def set_memory(key: str, value: dict):
    """Сохранение данных по ключу"""
    memory_manager.set_memory(key, value)
    return {"message": "Data saved successfully", "key": key}

# Маршрут для удаления данных из памяти по ключу
@router.delete("/memory/{key}")
async def delete_memory(key: str):
    """Удаление данных по ключу"""
    memory_manager.delete_memory(key)
    return {"message": "Data deleted successfully", "key": key}

# Маршрут для генерации текста с помощью OpenAI GPT
@router.post("/generate-text/")
async def generate_text_route(prompt: str, max_tokens: int = 150):
    """API для генерации текста с помощью OpenAI GPT"""
    try:
        generated_text = generate_text(prompt, max_tokens)
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

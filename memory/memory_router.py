from fastapi import APIRouter, HTTPException
from memory.memory_manager import MemoryManager
from memory.vector_manager import VectorManager

router = APIRouter()

# Инициализация памяти и векторов
memory_manager = MemoryManager()
vector_manager = VectorManager()

@router.post("/save_data/")
def save_data(key: str, value: str):
    """Сохраняет данные в память"""
    try:
        memory_manager.save_to_memory(key, value)
        return {"message": "Data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/retrieve_data/{key}")
def retrieve_data(key: str):
    """Извлекает данные из памяти"""
    data = memory_manager.retrieve_from_memory(key)
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"data": data}

@router.post("/add_vector/")
def add_vector(key: str, vector: list):
    """Добавляет вектор в память"""
    try:
        vector_manager.add_vector(key, vector)
        return {"message": "Vector added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calculate_similarity/{key1}/{key2}")
def calculate_similarity(key1: str, key2: str):
    """Вычисляет схожесть между двумя векторами"""
    similarity = vector_manager.calculate_similarity(key1, key2)
    return {"similarity": similarity}

# D:\AI_Coordinator_Project\api\handlers\ai_handler.py

from fastapi import APIRouter, HTTPException
from server.ai_interface import AIInterface
import logging

# Создание роутера для работы с запросами к AI
router = APIRouter()
ai_interface = AIInterface()

@router.post("/process")
async def process_request(request: dict):
    """
    Обрабатывает запросы, отправленные к AI интерфейсу.
    
    :param request: dict - Запрос, содержащий тип и параметры.
    :return: dict - Результат обработки.
    """
    if "request_type" not in request or "params" not in request:
        raise HTTPException(status_code=400, detail="Invalid request format. 'request_type' and 'params' are required.")
    
    request_type = request["request_type"]
    params = request["params"]

    try:
        # Передача запроса в AIInterface с использованием await для асинхронного вызова
        response = await ai_interface.handle_request(request_type, params)

        # Проверка на наличие ошибки в ответе
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])

        return response
    
    except Exception as e:
        # Логирование ошибки и генерация исключения с сообщением
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@router.get("/status")
async def get_status():
    """
    Проверяет текущий статус работы AI интерфейса.
    
    :return: dict - Статус ИИ.
    """
    return {"status": "AI Interface is operational"}

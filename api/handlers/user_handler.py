import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Any, Dict, Optional
from sqlalchemy.exc import SQLAlchemyError
from database.models.user import User
from database.database_manager import get_db_session
import logging
import openai
from memory.memory_manager import memory_manager  # Импортируем менеджер памяти

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Создание экземпляра APIRouter
router = APIRouter()

# Чтение ключа API из конфигурационного файла
def get_openai_api_key():
    config_path = "D:/AI_Coordinator_Project/config/openai_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["openai_api_key"]

# Подключение OpenAI API
openai.api_key = get_openai_api_key()

# Pydantic-модель для создания пользователя
class UserCreate(BaseModel):
    name: str
    email: EmailStr

# Pydantic-модель для успешного ответа
class UserResponse(BaseModel):
    message: str
    user: Dict[str, Any]

# Pydantic-модель для ошибок
class ErrorResponse(BaseModel):
    detail: str

# Модель для запроса генерации текста
class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 150
    temperature: float = 0.7

class TextGenerationResponse(BaseModel):
    generated_text: str

# Модель для ответа с данными из памяти
class MemoryResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None

# Эндпоинт для создания пользователя
@router.post("/", response_model=UserResponse, responses={
    400: {"model": ErrorResponse, "description": "User with this email already exists."},
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def create_user(user: UserCreate):
    session = get_db_session()
    try:
        existing_user = session.query(User).filter(User.email == user.email).first()
        if existing_user:
            logger.warning(f"User with email '{user.email}' already exists.")
            raise HTTPException(status_code=400, detail="User with this email already exists.")

        # Создание нового пользователя
        user_entry = User(name=user.name, email=user.email)
        session.add(user_entry)
        session.commit()
        session.refresh(user_entry)  # Обновляем объект, чтобы получить ID

        logger.info(f"User '{user.email}' successfully created.")
        return {
            "message": "User created successfully",
            "user": {"id": user_entry.id, "name": user_entry.name, "email": user_entry.email}
        }
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error during user creation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        session.close()

# Эндпоинт для очистки всех пользователей
@router.delete("/clear", status_code=204)
def clear_users():
    session = get_db_session()
    try:
        session.query(User).delete()
        session.commit()
        logger.info("All users have been successfully cleared.")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error during clearing users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        session.close()

# Эндпоинт для получения пользователя по ID
@router.get("/{user_id}", response_model=UserResponse, responses={
    404: {"model": ErrorResponse, "description": "User not found."},
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def get_user(user_id: int):
    session = get_db_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User with ID '{user_id}' not found.")
            raise HTTPException(status_code=404, detail="User not found.")

        logger.info(f"User '{user.email}' retrieved successfully.")
        return {
            "message": "User retrieved successfully",
            "user": {"id": user.id, "name": user.name, "email": user.email}
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        session.close()

# Эндпоинт для генерации текста с использованием OpenAI
@router.post("/generate-text", response_model=TextGenerationResponse, responses={
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def generate_text(request: TextGenerationRequest):
    try:
        # Подключение к OpenAI API и запрос на генерацию текста
        openai.api_key = get_openai_api_key()

        response = openai.Completion.create(
            engine="text-davinci-003",  # Укажите модель, которую хотите использовать
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        generated_text = response.choices[0].text.strip()
        logger.info(f"Text generated successfully: {generated_text}")
        return {"generated_text": generated_text}

    except openai.error.OpenAIError as e:
        logger.error(f"Error generating text with OpenAI: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    except Exception as e:
        logger.error(f"Unexpected error generating text: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

# Эндпоинт для получения данных из памяти
@router.get("/memory/{key}", response_model=MemoryResponse)
def get_memory(key: str):
    data = memory_manager.get_memory(key)
    if data is None:
        raise HTTPException(status_code=404, detail="Memory not found for the given key.")
    return {"status": "success", "message": f"Data for key '{key}' retrieved successfully.", "data": data}

# Эндпоинт для записи данных в память
@router.post("/memory", response_model=MemoryResponse)
def set_memory(key: str, value: dict):
    memory_manager.set_memory(key, value)
    return {"status": "success", "message": f"Data for key '{key}' set successfully."}

# Эндпоинт для удаления данных из памяти
@router.delete("/memory/{key}", response_model=MemoryResponse)
def delete_memory(key: str):
    memory_manager.delete_memory(key)
    return {"status": "success", "message": f"Data for key '{key}' deleted successfully."}
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from database.models.log import Log
from database.database_manager import get_db_session
import logging

# Инициализация логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Pydantic-модель для ответа
class LogResponse(BaseModel):
    id: int
    message: str
    level: str
    timestamp: str

# Модель для ошибок
class ErrorResponse(BaseModel):
    detail: str

@router.get("/", response_model=List[LogResponse], responses={
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def get_logs():
    """
    Получение списка логов из базы данных.
    """
    try:
        with get_db_session() as session:
            logs = session.query(Log).all()
            if not logs:
                logger.debug("No logs found in the database.")
                return []

            logger.debug(f"{len(logs)} logs retrieved successfully.")
            return [
                {"id": log.id, "message": log.message, "level": log.level, "timestamp": log.timestamp.isoformat()}
                for log in logs
            ]
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

# Инициализация логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Pydantic-модель для входных данных
class DataRequest(BaseModel):
    data: dict

# Pydantic-модель для успешного ответа
class DataResponse(BaseModel):
    message: str
    processed_data: dict

# Модель для ошибок
class ErrorResponse(BaseModel):
    detail: str

@router.post("/", response_model=DataResponse, responses={
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def process_data(data_request: DataRequest):
    """
    Пример обработки данных.
    """
    try:
        # Пример обработки данных
        processed_data = {key: str(value).upper() for key, value in data_request.data.items()}

        logger.info("Data processed successfully.")
        return {"message": "Data processed successfully", "processed_data": processed_data}
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

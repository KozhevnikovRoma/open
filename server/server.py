import sys
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging

# Добавление корневой папки проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импорт роутеров
from api.handlers.user_handler import router as user_router
from api.handlers.data_handler import router as data_router
from api.handlers.log_handler import router as log_router
from api.handlers.memory_router import router as memory_router
from api.handlers.ai_handler import router as ai_router  # Новый импорт для AI маршрута
from config.config_manager import Config  # Подключение конфигурации

# Настройка логирования
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(LOG_DIR, exist_ok=True)  # Создаем папку для логов, если ее нет

LOG_PATH = os.path.join(LOG_DIR, "server_logs.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_PATH),  # Обработчик для записи в файл
        logging.StreamHandler()  # Обработчик для вывода в консоль
    ]
)

# Создание экземпляра FastAPI
app = FastAPI()

# Загружаем конфигурацию
config = Config()

# Подключение роутеров с префиксами для каждой группы
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(data_router, prefix="/data", tags=["Data"])
app.include_router(log_router, prefix="/logs", tags=["Logs"])
app.include_router(memory_router, prefix="/memory", tags=["Memory"])
app.include_router(ai_router, prefix="/ai", tags=["AI"])  # Подключение AI маршрута

@app.get("/project_status")
def get_project_status():
    """Эндпоинт для проверки состояния проекта."""
    return {"status": "success", "message": "Проект успешно запущен и доступен!"}

@app.get("/")
def read_root():
    """Тестовый эндпоинт для проверки работы сервера."""
    logging.info("Root endpoint accessed")  # Логирование информации о доступе
    return {"message": "AI Coordinator Server is running!"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Обработка глобальных исключений."""
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    try:
        host = config.SERVER_HOST
        port = config.SERVER_PORT
        logging.info(f"Starting the server on {host}:{port}")
        uvicorn.run("server.server:app", host=host, port=port, reload=True)
    except Exception as e:
        logging.critical(f"Failed to start the server: {e}", exc_info=True)

from sqlalchemy import create_engine, inspect
from database.database_manager import DatabaseManager  # Абсолютный импорт DatabaseManager
from database.models.user import User  # Абсолютный импорт модели User
from database.models.task import Task  # Абсолютный импорт модели Task
from database.models.log import Log  # Абсолютный импорт модели Log
from sqlalchemy.orm import sessionmaker

def run_migrations():
    """
    Запустить миграции для базы данных.
    Обновить схему базы данных, добавив недостающие столбцы.
    """
    # Создание подключения к базе данных
    db_manager = DatabaseManager()
    engine = db_manager.get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Получаем текущую схему таблиц
    inspector = inspect(engine)
    
    # Проверяем наличие таблицы users и колонок created_at, updated_at
    if "users" in inspector.get_table_names():
        columns = [column["name"] for column in inspector.get_columns("users")]
        if "created_at" not in columns:
            print("Добавление столбца created_at в таблицу users.")
            # Добавляем столбец created_at
            with engine.connect() as conn:
                conn.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

        if "updated_at" not in columns:
            print("Добавление столбца updated_at в таблицу users.")
            # Добавляем столбец updated_at
            with engine.connect() as conn:
                conn.execute("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    
    # Создание таблиц, если их нет
    db_manager.create_tables()
    print("Миграции выполнены успешно!")

if __name__ == "__main__":
    run_migrations()

import os
import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем URL базы данных из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Ошибка: DATABASE_URL не найден в .env файле.")
    exit(1)

# Создаем соединение с базой данных
engine = create_engine(DATABASE_URL, echo=True)

# Анализируем структуру базы данных
def analyze_database_structure(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if tables:
        print("Таблицы в базе данных:")
        for table in tables:
            print(f"- {table}")
    else:
        print("В базе данных нет таблиц.")

if __name__ == "__main__":
    analyze_database_structure(engine)

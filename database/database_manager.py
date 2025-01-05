from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Создаем общий Base для всех моделей
Base = declarative_base()

class DatabaseManager:
    def __init__(self):
        # Читаем URL базы данных из переменной окружения
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///ai_coordinator.db")
        self.engine = create_engine(self.database_url, echo=True)  # Включаем логгирование SQL-запросов для отладки
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """
        Создаёт таблицы, если они ещё не существуют.
        """
        inspector = inspect(self.engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:
            print("Creating all tables...")
            Base.metadata.create_all(self.engine)
            print("All tables have been created successfully.")
        else:
            print(f"Tables already exist: {existing_tables}")

    def drop_tables(self):
        """
        Удаляет все таблицы в базе данных. Использовать с осторожностью.
        """
        print("Dropping all tables...")
        Base.metadata.drop_all(self.engine)
        print("All tables have been dropped successfully.")

    def reset_tables(self):
        """
        Полностью сбрасывает таблицы: удаляет и пересоздаёт.
        """
        self.drop_tables()
        self.create_tables()

    def get_session(self):
        """
        Создаёт сессию для работы с базой данных.
        """
        return self.Session()

# Функция для получения сессии
def get_db_session():
    """
    Фабричный метод для создания сессии через DatabaseManager.
    """
    db_manager = DatabaseManager()
    return db_manager.get_session()

if __name__ == "__main__":
    db_manager = DatabaseManager()

    # Создать таблицы, если они ещё не существуют
    db_manager.create_tables()

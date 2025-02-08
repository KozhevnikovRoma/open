from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import json
import logging
from dotenv import load_dotenv  # Импортируем dotenv для загрузки .env

# Загружаем переменные окружения из файла .env
load_dotenv()

# Настройка логирования
logging.basicConfig(filename="database.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Загружаем конфиг
CONFIG_PATH = "database/db_config.json"

def load_config():
    try:
        with open(CONFIG_PATH, "r") as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Ошибка загрузки конфигурации: {e}")
        return {"DATABASE_URL": "sqlite:///ai_coordinator.db"}  # Значение по умолчанию

config = load_config()
DATABASE_URL = config.get("DATABASE_URL", "sqlite:///ai_coordinator.db")

# Печатаем DATABASE_URL для проверки
print(f"DATABASE_URL: {DATABASE_URL}")

# SQLAlchemy настройки
Base = declarative_base()

class DatabaseManager:
    def __init__(self):
        try:
            self.engine = create_engine(DATABASE_URL, echo=False)  # echo=False, чтобы не засорять вывод
            self.Session = sessionmaker(bind=self.engine)
            logging.info(f"Подключение к БД: {DATABASE_URL}")
        except Exception as e:
            logging.error(f"Ошибка при подключении к базе данных: {e}")

    def create_tables(self):
        """Создаёт таблицы, если они ещё не существуют."""
        try:
            inspector = inspect(self.engine)
            existing_tables = inspector.get_table_names()

            if not existing_tables:
                logging.info("Создание таблиц...")
                Base.metadata.create_all(self.engine)
                logging.info("Все таблицы успешно созданы.")
            else:
                logging.info(f"Таблицы уже существуют: {existing_tables}")
        except Exception as e:
            logging.error(f"Ошибка при создании таблиц: {e}")

    def drop_tables(self):
        """Удаляет все таблицы (использовать осторожно!)."""
        try:
            logging.warning("Удаление всех таблиц...")
            Base.metadata.drop_all(self.engine)
            logging.info("Все таблицы удалены.")
        except Exception as e:
            logging.error(f"Ошибка при удалении таблиц: {e}")

    def reset_tables(self):
        """Полностью сбрасывает таблицы: удаляет и пересоздаёт."""
        self.drop_tables()
        self.create_tables()

    def get_session(self):
        """Создаёт сессию для работы с БД."""
        return self.Session()

    # Методы работы с данными
    def add_data(self, data):
        """Добавляет данные в таблицу."""
        session = self.get_session()
        try:
            session.add(data)
            session.commit()
            logging.info(f"Данные добавлены: {data}")
        except Exception as e:
            session.rollback()
            logging.error(f"Ошибка при добавлении данных: {e}")
        finally:
            session.close()

    def get_data(self, model, filters=None):
        """Получает данные из таблицы."""
        session = self.get_session()
        try:
            query = session.query(model)
            if filters:
                query = query.filter_by(**filters)
            result = query.all()
            logging.info(f"Данные получены: {result}")
            return result
        except Exception as e:
            logging.error(f"Ошибка при получении данных: {e}")
        finally:
            session.close()

    def update_data(self, model, filters, update_values):
        """Обновляет данные в таблице."""
        session = self.get_session()
        try:
            query = session.query(model).filter_by(**filters)
            updated_count = query.update(update_values)
            session.commit()
            logging.info(f"Обновлено записей: {updated_count}")
        except Exception as e:
            session.rollback()
            logging.error(f"Ошибка при обновлении данных: {e}")
        finally:
            session.close()

    def delete_data(self, model, filters):
        """Удаляет данные из таблицы."""
        session = self.get_session()
        try:
            query = session.query(model).filter_by(**filters)
            deleted_count = query.delete()
            session.commit()
            logging.info(f"Удалено записей: {deleted_count}")
        except Exception as e:
            session.rollback()
            logging.error(f"Ошибка при удалении данных: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_tables()

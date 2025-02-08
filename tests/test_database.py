from database.database_manager import DatabaseManager
from database.models import User

if __name__ == "__main__":
    db_manager = DatabaseManager()
    session = db_manager.get_session()

    # Добавляем пользователя
    new_user = User(name="Test User", email="test@example.com")
    session.add(new_user)
    session.commit()

    print("Пользователь добавлен!")

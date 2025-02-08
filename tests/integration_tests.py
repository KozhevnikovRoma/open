import unittest
from fastapi.testclient import TestClient
from server.server import app
from database.models.user import User
from database.database_manager import DatabaseManager
from database.database_manager import get_db_session

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Инициализация тестового клиента и подготовка БД"""
        self.client = TestClient(app)
        self.db_manager = DatabaseManager()  # Убедитесь, что инициализация таблиц правильная
        self.db_manager.create_tables()  # Создание таблиц
        self.session = get_db_session()  # Получаем сессию для работы с БД

        # Очистка таблицы пользователей перед тестами
        self.session.query(User).delete()
        self.session.commit()

    def test_create_and_get_user(self):
        """Проверка создания и получения пользователя через API"""
        # Тест создания пользователя
        response = self.client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("User created successfully", response.json()["message"])

        # Тест получения пользователя по ID
        user_id = 1  # Предполагаем, что это первый пользователь
        response = self.client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "John Doe")
        self.assertEqual(response.json()["email"], "john@example.com")

    def tearDown(self):
        """Очистка БД после тестов"""
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

if __name__ == "__main__":
    unittest.main()

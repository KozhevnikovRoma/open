# D:\AI_Coordinator_Project\tests\test_user_handler.py

import pytest
from fastapi.testclient import TestClient
from server.server import app  # Импортируем экземпляр FastAPI из server.py

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Фикстура для очистки данных перед каждым тестом.
    Предполагается, что API имеет эндпоинт очистки для тестов (например, /users/clear).
    """
    client.delete("/users/clear")
    yield

def test_create_user():
    """Тест создания пользователя"""
    response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "User created successfully"
    assert response_data["user"]["name"] == "John Doe"
    assert response_data["user"]["email"] == "john@example.com"

def test_create_user_duplicate():
    """Тест создания пользователя с дублирующимся email"""
    client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    response = client.post("/users/", json={"name": "Jane Doe", "email": "john@example.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User with this email already exists."}

def test_get_user():
    """Тест получения существующего пользователя"""
    create_response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    user_id = create_response.json()["user"]["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user_id
    assert response_data["name"] == "John Doe"
    assert response_data["email"] == "john@example.com"

def test_get_user_not_found():
    """Тест получения несуществующего пользователя"""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}

@pytest.mark.parametrize("user_data, expected_status, expected_response", [
    ({"name": "John", "email": "john@example.com"}, 200, {"message": "User created successfully"}),
    ({"name": "", "email": "john@example.com"}, 400, {"detail": "Name must not be empty."}),
    ({"name": "John", "email": "invalid_email"}, 400, {"detail": "Invalid email format."}),
])
def test_create_user_validation(user_data, expected_status, expected_response):
    """Тест валидации данных при создании пользователя"""
    response = client.post("/users/", json=user_data)
    assert response.status_code == expected_status
    if response.status_code == 200:
        assert response.json()["message"] == expected_response["message"]
    else:
        assert response.json() == expected_response

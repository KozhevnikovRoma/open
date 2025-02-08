import pytest
from fastapi.testclient import TestClient
from server.server import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    client.delete("/users/clear")
    yield
    client.delete("/users/clear")

def test_create_user():
    response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"
    assert "user" in response.json()
    assert "id" in response.json()["user"]

def test_create_user_duplicate():
    client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    response = client.post("/users/", json={"name": "Jane Doe", "email": "john@example.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User with this email already exists."}

def test_get_user():
    create_response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    assert create_response.status_code == 200
    user = create_response.json()["user"]
    assert "id" in user

    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json()["user"] == user

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}

def test_clear_users():
    client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    client.post("/users/", json={"name": "Jane Doe", "email": "jane@example.com"})
    clear_response = client.delete("/users/clear")
    assert clear_response.status_code == 204

    get_response = client.get("/users/1")
    assert get_response.status_code == 404

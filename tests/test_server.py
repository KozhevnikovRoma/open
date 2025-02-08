from fastapi.testclient import TestClient
from server.server import app

def test_server_running():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Coordinator Server is running!"}

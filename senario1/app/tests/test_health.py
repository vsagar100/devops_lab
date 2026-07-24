from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200


def test_orders():
    response = client.get("/api/orders")
    assert response.status_code == 200


def test_error():
    response = client.get("/api/error")
    assert response.status_code == 500

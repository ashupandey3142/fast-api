import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_employee():
    employee_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "salary": 50000,
        "password": "securepassword"
    }
    response = client.post("/employee", json=employee_data)
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert "id" in response.json()


def test_get_employee():
    response = client.get("/employee/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_employees():
    response = client.get("/employee")
    assert response.status_code == 200
    assert len(response.json()) > 0


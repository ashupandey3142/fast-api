from fastapi.testclient import TestClient
from main import app
import pytest


# @pytest.fixture() is beneficial when you want to perform setup or provide dynamic instances that might vary between tests.
# It allows for more flexibility and avoids global state changes that might affect other tests.
@pytest.fixture()
def client():
    return TestClient(app)


def test_create_item(client: TestClient):
    response = client.post("/items/", json={"name": "item1", "description": "test"})
    assert response.status_code == 200
    assert response.json()["name"] == "item1"
    assert response.json()["description"] == "test"


def test_read_items(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1  # One item was created in the previous test


def test_read_item(client: TestClient):
    response = client.get("/items/0")
    assert response.status_code == 200
    assert response.json()["name"] == "item1"
    assert response.json()["description"] == "test"


def test_update_item(client: TestClient):
    response = client.put("/items/0", json={"name": "item_updated", "description": "updated_test"})
    assert response.status_code == 200
    assert response.json()["name"] == "item_updated"
    assert response.json()["description"] == "updated_test"


def test_delete_item(client: TestClient):
    response = client.delete("/items/0")
    assert response.status_code == 200
    assert response.json()["name"] == "item_updated"
    assert response.json()["description"] == "updated_test"


def test_read_items_after_delete(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 0  # No items after deletion


def test_read_nonexistent_item(client: TestClient):
    response = client.get("/items/0")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_update_nonexistent_item(client: TestClient):
    response = client.put("/items/0", json={"name": "item_updated", "description": "updated_test"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_delete_nonexistent_item(client: TestClient):
    response = client.delete("/items/0")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

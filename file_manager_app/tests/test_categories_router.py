from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_create_category(auth_headers):
    resp = client.post("/categories/", json={"name": "Groceries"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Groceries"


def test_get_category(auth_headers):
    # Create category first
    resp = client.post("/categories/", json={"name": "Transport"}, headers=auth_headers)
    category_id = resp.json()["id"]
    resp = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Transport"


def test_list_categories(auth_headers):
    resp = client.get("/categories/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_update_category(auth_headers):
    # Create category first
    resp = client.post("/categories/", json={"name": "Bills"}, headers=auth_headers)
    category_id = resp.json()["id"]
    # Update category
    resp = client.put(f"/categories/{category_id}", json={"name": "Utilities"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Utilities"


def test_delete_category(auth_headers):
    # Create category first
    resp = client.post("/categories/", json={"name": "DeleteMe"}, headers=auth_headers)
    category_id = resp.json()["id"]
    # Delete category
    resp = client.delete(f"/categories/DeleteMe", headers=auth_headers)
    assert resp.status_code == 200
    # Ensure it's gone
    resp = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert resp.status_code == 404
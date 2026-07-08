import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def auth_headers():
    # Register and login a user, return headers with JWT token
    user = {"username": "testuser", "password": "testpass"}
    client.post("/register", json=user)
    resp = client.post("/token", data=user)
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
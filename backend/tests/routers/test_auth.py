import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.models import User
from backend.models.enums import UserRole
from backend.dependencies.auth_utils import get_password_hash

def test_login_success(client, test_user):
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, test_user):
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_nonexistent_user(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

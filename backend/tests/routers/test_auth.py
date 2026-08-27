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
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, status
from backend.routers.auth import fetch_google_certs

def test_fetch_google_certs_error():
    # Clear the global cache to force fetching
    import backend.routers.auth as auth
    auth._certs_cache = {}
    auth._certs_expiry = 0

    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = Exception("Network error")

        with pytest.raises(HTTPException) as exc_info:
            fetch_google_certs()

        assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert exc_info.value.detail == "Failed to retrieve Google authentication certificates"

def test_fetch_google_certs_timeout():
    import backend.routers.auth as auth
    auth._certs_cache = {}
    auth._certs_expiry = 0
    import urllib.error

    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("Timeout")

        with pytest.raises(HTTPException) as exc_info:
            fetch_google_certs()

        assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert exc_info.value.detail == "Failed to retrieve Google authentication certificates"

def test_fetch_google_certs_success():
    import backend.routers.auth as auth
    auth._certs_cache = {}
    auth._certs_expiry = 0
    import json

    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({"key1": "cert1", "key2": "cert2"}).encode('utf-8')

    # Needs to be able to be used in 'with' statement
    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = mock_response
    mock_context_manager.__exit__.return_value = None

    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.return_value = mock_context_manager

        result = fetch_google_certs()

        assert result == {"key1": "cert1", "key2": "cert2"}
        assert auth._certs_cache == {"key1": "cert1", "key2": "cert2"}
        assert auth._certs_expiry > 0

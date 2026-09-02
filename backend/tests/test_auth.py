from fastapi import status
from datetime import datetime, timezone
from backend.models.models import User
from backend.models.enums import UserRole
from backend.dependencies.auth_utils import get_password_hash

def test_signup_success(client, db_session):
    response = client.post(
        "/api/auth/signup",
        json={"email": "newuser@example.com", "password": "securepassword", "role": "CANDIDATE"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "CANDIDATE"
    assert data["profile_completed"] is False

    # Check if user is in DB
    user = db_session.query(User).filter(User.email == "newuser@example.com").first()
    assert user is not None

def test_signup_existing_email(client, db_session):
    # Insert existing user
    user = User(
        email="existing@example.com",
        hashed_password=get_password_hash("securepassword"),
        role=UserRole.CANDIDATE,
        profile_completed=False
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/signup",
        json={"email": "existing@example.com", "password": "securepassword", "role": "CANDIDATE"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"


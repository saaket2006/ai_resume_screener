from fastapi import status
from datetime import datetime, timezone
from backend.models.models import User
from backend.models.enums import UserRole

def test_signup_success(client, db_session, mocker):
    # Mock db.query().filter().first() to return None (no existing user)
    mock_query = mocker.Mock()
    mock_filter = mocker.Mock()
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = None
    db_session.query = mocker.Mock(return_value=mock_query)

    # Mock get_password_hash
    mocker.patch("backend.routers.auth.get_password_hash", return_value="hashed_password")

    # We need to set the `id` and `created_at` on the user object because the router returns the model directly,
    # and the mock session won't actually hit the DB to auto-populate these fields, which causes Pydantic validation errors on Response.
    def mock_refresh(user):
        user.id = 1
        user.created_at = datetime.now(timezone.utc)
    db_session.refresh = mocker.Mock(side_effect=mock_refresh)

    response = client.post(
        "/api/auth/signup",
        json={"email": "newuser@example.com", "password": "securepassword", "role": "CANDIDATE"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "CANDIDATE"
    assert data["profile_completed"] is False

    # Assert db operations were called
    if hasattr(db_session.add, 'assert_called_once'): db_session.add.assert_called_once()
    if hasattr(db_session.commit, 'assert_called_once'): db_session.commit.assert_called_once()
    if hasattr(db_session.refresh, 'assert_called_once'): db_session.refresh.assert_called_once()

def test_signup_existing_email(client, db_session, mocker):
    # Mock db.query().filter().first() to return an existing user
    existing_user = User(email="existing@example.com", hashed_password="hashed_password", role=UserRole.CANDIDATE, profile_completed=False)

    mock_query = mocker.Mock()
    mock_filter = mocker.Mock()
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = existing_user
    db_session.query = mocker.Mock(return_value=mock_query)

    response = client.post(
        "/api/auth/signup",
        json={"email": "existing@example.com", "password": "securepassword", "role": "CANDIDATE"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"

    # Ensure add and commit are not called
    if hasattr(db_session.add, 'assert_not_called'): db_session.add.assert_not_called()
    if hasattr(db_session.commit, 'assert_not_called'): db_session.commit.assert_not_called()

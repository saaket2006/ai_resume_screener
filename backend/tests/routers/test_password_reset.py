import datetime
import hashlib
import secrets
from unittest.mock import patch
import pytest
from backend.models.models import User, PasswordResetToken
from backend.models.enums import UserRole
from backend.dependencies.auth_utils import get_password_hash, verify_password

from backend.limiter import limiter


@pytest.fixture(autouse=True)
def disable_rate_limiting():
    """Temporarily disables SlowAPI rate limiting for unit tests."""
    limiter.enabled = False
    yield
    limiter.enabled = True


@pytest.fixture
def existing_user(db_session):
    """Creates an existing user for testing password reset flows."""
    user = User(
        email="reset_target@example.com",
        hashed_password=get_password_hash("OriginalPassword123!"),
        role=UserRole.CANDIDATE,
        profile_completed=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ==============================================================================
# FORGOT PASSWORD TESTS
# ==============================================================================

def test_forgot_password_existing_user(client, db_session, existing_user):
    """Test requesting a reset link for an existing user."""
    with patch("backend.routers.auth.send_password_reset_email") as mock_send_email:
        response = client.post(
            "/api/auth/forgot-password",
            json={"email": "reset_target@example.com"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "If an account exists for this email, a password reset link has been sent."

        # Verify email dispatch was triggered
        assert mock_send_email.called
        call_args = mock_send_email.call_args[0]
        assert call_args[0] == "reset_target@example.com"
        reset_link = call_args[1]
        assert "/#/reset-password?token=" in reset_link

        # Verify token was created in DB
        tokens = db_session.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == existing_user.id
        ).all()
        assert len(tokens) == 1
        token_record = tokens[0]
        assert token_record.is_used is False
        assert token_record.expires_at > datetime.datetime.utcnow()

        # Security check: verify raw token is NOT stored in DB
        raw_token = reset_link.split("token=")[1]
        assert raw_token != token_record.token_hash
        assert hashlib.sha256(raw_token.encode("utf-8")).hexdigest() == token_record.token_hash


def test_forgot_password_nonexistent_user(client, db_session):
    """Test enumeration protection: non-existent email returns identical success message."""
    with patch("backend.routers.auth.send_password_reset_email") as mock_send_email:
        response = client.post(
            "/api/auth/forgot-password",
            json={"email": "nobody@example.com"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "If an account exists for this email, a password reset link has been sent."
        # No email should be sent for nonexistent user
        assert not mock_send_email.called


def test_forgot_password_malformed_email(client):
    """Test validation rejection for invalid email syntax."""
    response = client.post(
        "/api/auth/forgot-password",
        json={"email": "not-an-email"}
    )
    assert response.status_code == 422


def test_forgot_password_invalidates_prior_tokens(client, db_session, existing_user):
    """Test that requesting a new reset token invalidates older unused tokens."""
    with patch("backend.routers.auth.send_password_reset_email"):
        # First request
        client.post("/api/auth/forgot-password", json={"email": "reset_target@example.com"})
        # Second request
        client.post("/api/auth/forgot-password", json={"email": "reset_target@example.com"})

        tokens = db_session.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == existing_user.id
        ).order_by(PasswordResetToken.id.asc()).all()

        assert len(tokens) == 2
        # First token must be marked used/invalidated
        assert tokens[0].is_used is True
        # Second token must be active
        assert tokens[1].is_used is False


# ==============================================================================
# RESET PASSWORD TESTS
# ==============================================================================

def test_reset_password_success(client, db_session, existing_user):
    """Test resetting password with a valid token."""
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    reset_token = PasswordResetToken(
        user_id=existing_user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        is_used=False
    )
    db_session.add(reset_token)
    db_session.commit()

    # Perform password reset
    response = client.post(
        "/api/auth/reset-password",
        json={"token": raw_token, "new_password": "NewSecurePassword456!"}
    )
    assert response.status_code == 200
    assert "successfully reset" in response.json()["message"]

    # Token must now be marked used
    db_session.refresh(reset_token)
    assert reset_token.is_used is True

    # Check database user password hash
    db_session.refresh(existing_user)
    assert verify_password("NewSecurePassword456!", existing_user.hashed_password)
    assert not verify_password("OriginalPassword123!", existing_user.hashed_password)
    assert existing_user.hashed_password.startswith("$2b$")  # bcrypt hash verification

    # Verify login with old password fails
    old_login_resp = client.post(
        "/api/auth/login",
        json={"email": "reset_target@example.com", "password": "OriginalPassword123!"}
    )
    assert old_login_resp.status_code == 401

    # Verify login with new password succeeds
    new_login_resp = client.post(
        "/api/auth/login",
        json={"email": "reset_target@example.com", "password": "NewSecurePassword456!"}
    )
    assert new_login_resp.status_code == 200
    assert "access_token" in new_login_resp.json()


def test_reset_password_single_use(client, db_session, existing_user):
    """Test that a reset token cannot be reused a second time."""
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    reset_token = PasswordResetToken(
        user_id=existing_user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        is_used=False
    )
    db_session.add(reset_token)
    db_session.commit()

    # First reset succeeds
    resp1 = client.post(
        "/api/auth/reset-password",
        json={"token": raw_token, "new_password": "FirstNewPassword123!"}
    )
    assert resp1.status_code == 200

    # Second reset with the same token fails
    resp2 = client.post(
        "/api/auth/reset-password",
        json={"token": raw_token, "new_password": "SecondNewPassword123!"}
    )
    assert resp2.status_code == 400
    assert resp2.json()["detail"] == "Invalid or expired reset token."


def test_reset_password_expired_token(client, db_session, existing_user):
    """Test that an expired token is rejected."""
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    # Expired 10 minutes ago
    expires_at = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

    reset_token = PasswordResetToken(
        user_id=existing_user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        is_used=False
    )
    db_session.add(reset_token)
    db_session.commit()

    response = client.post(
        "/api/auth/reset-password",
        json={"token": raw_token, "new_password": "NewSecurePassword456!"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired reset token."


def test_reset_password_invalid_token(client):
    """Test that an unknown/tampered token string is rejected."""
    response = client.post(
        "/api/auth/reset-password",
        json={"token": "completely_invalid_token_string", "new_password": "NewSecurePassword456!"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired reset token."


def test_reset_password_short_password(client):
    """Test that a new password shorter than 8 characters is rejected by schema."""
    response = client.post(
        "/api/auth/reset-password",
        json={"token": "some_token", "new_password": "short"}
    )
    assert response.status_code == 422


# ==============================================================================
# SECURITY & ENUMERATION PROTECTION TESTS
# ==============================================================================

def test_enumeration_protection_identical_response(client, existing_user):
    """Ensure forgot-password responses for existing vs non-existent users are identical."""
    with patch("backend.routers.auth.send_password_reset_email"):
        resp_existing = client.post(
            "/api/auth/forgot-password",
            json={"email": existing_user.email}
        )
        resp_nonexistent = client.post(
            "/api/auth/forgot-password",
            json={"email": "definitely_nonexistent_email_12345@example.com"}
        )

        assert resp_existing.status_code == 200
        assert resp_nonexistent.status_code == 200
        assert resp_existing.json() == resp_nonexistent.json()

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.main import app
from backend.database.database import get_db

@pytest.fixture
def mock_db_session(mocker):
    session = mocker.Mock(spec=Session)
    # create a basic mock for query
    return session

@pytest.fixture
def client(mock_db_session):
    def override_get_db():
        yield mock_db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

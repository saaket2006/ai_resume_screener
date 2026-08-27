import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from backend.routers.recruiter import create_job_description
from backend.models.models import User, JobDescription

def test_create_job_description_success():
    # Setup mocks
    mock_db = MagicMock(spec=Session)
    mock_user = MagicMock(spec=User)
    mock_user.id = 1

    # Run function
    result = create_job_description(
        title="Software Engineer",
        subtitle="Backend",
        description="Write code",
        company="Tech Inc",
        optional_notes="Urgent",
        current_user=mock_user,
        db=mock_db
    )

    # Assert result
    assert result["message"] == "Job description created successfully"
    assert "id" in result

    # Assert DB calls
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    # Check what was added
    added_obj = mock_db.add.call_args[0][0]
    assert isinstance(added_obj, JobDescription)
    assert added_obj.owner_id == 1
    assert added_obj.title == "Software Engineer"
    assert added_obj.subtitle == "Backend"
    assert added_obj.description == "Write code"
    assert added_obj.company == "Tech Inc"
    assert added_obj.optional_notes == "Urgent"

def test_create_job_description_minimal():
    # Setup mocks
    mock_db = MagicMock(spec=Session)
    mock_user = MagicMock(spec=User)
    mock_user.id = 1

    # Run function with only required fields
    result = create_job_description(
        title="Software Engineer",
        subtitle=None,
        description="Write code",
        company=None,
        optional_notes=None,
        current_user=mock_user,
        db=mock_db
    )

    # Assert result
    assert result["message"] == "Job description created successfully"
    assert "id" in result

    # Assert DB calls
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    # Check what was added
    added_obj = mock_db.add.call_args[0][0]
    assert isinstance(added_obj, JobDescription)
    assert added_obj.owner_id == 1
    assert added_obj.title == "Software Engineer"
    assert added_obj.subtitle is None
    assert added_obj.description == "Write code"
    assert added_obj.company is None
    assert added_obj.optional_notes is None

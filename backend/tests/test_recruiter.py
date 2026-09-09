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

from backend.routers.recruiter import get_recruiter_stats
from backend.models.models import ScanResult

def test_get_recruiter_stats_malformed_experience():
    # Setup mocks
    mock_db = MagicMock(spec=Session)
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.email = "recruiter@test.com"

    # Create mock scan results with malformed experience values
    # One with a bad string, one with an uncastable object, one with a valid float
    scan1 = MagicMock(spec=ScanResult)
    scan1.ats_score = 80
    scan1.analysis_metadata = {
        "candidate": {
            "experience": "Five years" # ValueError
        }
    }

    scan2 = MagicMock(spec=ScanResult)
    scan2.ats_score = 90
    scan2.analysis_metadata = {
        "candidate": {
            "experience": {"years": 5} # TypeError
        }
    }

    scan3 = MagicMock(spec=ScanResult)
    scan3.ats_score = 70
    scan3.analysis_metadata = {
        "candidate": {
            "experience": "5.5" # Valid
        }
    }

    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [scan1, scan2, scan3]

    # Run function
    result = get_recruiter_stats(
        current_user=mock_user,
        db=mock_db
    )

    # Assert results
    assert result["total_candidates_screened"] == 3
    assert result["average_ats_score"] == 80.0
    # Average experience should only count the valid "5.5" string -> 5.5 / 1 = 5.5
    assert result["average_experience_tenure"] == 5.5

import pytest
from unittest.mock import MagicMock
from backend.routers.recruiter import get_recruiter_stats
from backend.models.models import User

def test_get_recruiter_stats_empty_scans():
    # Mock user
    mock_user = User(id=1, email="test@example.com")

    # Mock db session
    mock_db = MagicMock()
    # Ensure that db.query(...).join(...).filter(...).all() returns an empty list
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []

    # Call the function
    result = get_recruiter_stats(current_user=mock_user, db=mock_db)

    # Assertions
    assert result["total_candidates_screened"] == 0
    assert result["average_ats_score"] == 0.0
    assert result["average_experience_tenure"] == 0.0
    assert result["most_common_education_level"] == "None"
    assert result["most_common_missing_skills"] == []
    assert result["most_common_matched_skills"] == []
    assert result["top_recommended_improvements"] == []
    assert result["education_breakdown"] == []

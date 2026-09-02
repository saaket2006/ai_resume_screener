import pytest
from backend.services.info_extractor import extract_experience

def test_extract_experience_standard_formats():
    """Test extracting experience with standard variations."""
    assert extract_experience("I have 5 years of experience in Python.") == 5
    assert extract_experience("10+ years experience") == 10
    assert extract_experience("3 yrs experience") == 3
    assert extract_experience("1 yr of experience") == 1
    assert extract_experience("Worked for 7 years of experience in AI.") == 7

def test_extract_experience_multiple_mentions():
    """Test extracting the maximum experience when mentioned multiple times."""
    assert extract_experience("2 years of experience here, and 5 years of experience there") == 5
    assert extract_experience("Had 10 years experience before getting 2 more years experience.") == 10

def test_extract_experience_no_match():
    """Test when no experience is mentioned."""
    assert extract_experience("I just graduated.") == 0
    assert extract_experience("I worked at a company.") == 0
    assert extract_experience("Many years of working.") == 0

def test_extract_experience_edge_cases():
    """Test edge cases with formatting and spacing."""
    assert extract_experience("12 + years of experience") == 12
    assert extract_experience("4+yrs experience") == 4
    assert extract_experience("15+ years experience") == 15
    assert extract_experience("My 0 years of experience") == 0
    assert extract_experience("I have twenty years of experience") == 0  # Assuming it only captures digits based on regex

def test_extract_experience_case_insensitivity():
    """Test case insensitivity."""
    assert extract_experience("5 YEARS OF EXPERIENCE") == 5
    assert extract_experience("5 Years Of Experience") == 5
    assert extract_experience("5 Yrs Experience") == 5

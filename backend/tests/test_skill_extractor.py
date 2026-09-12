import pytest
from backend.services.skill_extractor import extract_raw_skill_strings

def test_extract_raw_skill_strings():
    text = "We need someone with React and JavaScript experience, plus AWS."
    skills = extract_raw_skill_strings(text)
    assert "react" in skills
    assert "javascript" in skills
    assert "aws" in skills

    text_partial = "I have a reactor and a javascripted application."
    skills_partial = extract_raw_skill_strings(text_partial)
    assert "react" not in skills_partial
    assert "javascript" not in skills_partial

    # Test edge cases where skill is at the beginning or end
    skills_edge = extract_raw_skill_strings("React is great.")
    assert "react" in skills_edge

    skills_edge2 = extract_raw_skill_strings("I love React")
    assert "react" in skills_edge2

def test_extract_acronyms():
    text = "Familiar with REST and SOAP APIs."
    skills = extract_raw_skill_strings(text)
    assert "rest" in skills
    assert "soap" in skills

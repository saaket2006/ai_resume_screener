import pytest
from backend.services.xai.formatter import format_overall_explanation

def test_format_overall_explanation_summary():
    awarded, deducted = format_overall_explanation(85.5, "SUMMARY")
    assert "85.5%" in awarded
    assert "weighted average" in deducted

def test_format_overall_explanation_detailed():
    awarded, deducted = format_overall_explanation(90.2, "DETAILED")
    assert "90.2%" in awarded
    assert "constituent components" in awarded
    assert "Component gaps" in deducted

def test_format_overall_explanation_technical():
    awarded, deducted = format_overall_explanation(77.7, "TECHNICAL")
    assert "77.7%" in awarded
    assert "skill_score * 0.50" in awarded
    assert "linear combination" in deducted

def test_format_overall_explanation_other():
    awarded, deducted = format_overall_explanation(65.0, "UNKNOWN")
    assert "65.0%" in awarded
    assert "skill_score * 0.50" in awarded
    assert "linear combination" in deducted

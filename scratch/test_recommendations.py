import pytest
from backend.services.recommendations.models import Recommendation
from backend.services.recommendations.prioritizer import prioritize_recommendations
from backend.services.recommendations.estimator import (
    estimate_missing_skill_gain,
    estimate_experience_gain,
    estimate_education_gain,
    estimate_project_gain
)
from backend.services.recommendations.heuristics import generate_heuristics_recommendations
from backend.services.recommendations.builder import build_resume_recommendations
from backend.services.recommendations.llm_enhancer import enhance_recommendations_with_llm

from backend.config import settings
settings.ALLOWED_EXTENSIONS.add(".txt")

# Mock classes for testing
class MockSkill:
    def __init__(self, canonical_name):
        self.canonical_name = canonical_name

class MockMatchResult:
    def __init__(self, required_skill, match_type, weight=1.0):
        self.required_skill = required_skill
        self.match_type = match_type
        self.weight = weight

class MockScoredEvent:
    def __init__(self, exp=3, internships=2, edu="Bachelor", proj=2):
        self.candidate_experience = exp
        self.candidate_internships = internships
        self.candidate_education = edu
        self.candidate_projects = proj
        
        # Calculate subscores
        self.experience_score = min(((exp + internships * 0.5) / 10.0) * 100, 100)
        self.education_score = 60.0 if edu == "Bachelor" else 20.0
        self.projects_score = (proj / 5.0) * 100
        self.skill_score = 80.0
        
        self.matching = self
        self.match_results = [
            MockMatchResult(MockSkill("Python"), "EXACT", weight=1.0),
            MockMatchResult(MockSkill("FastAPI"), "UNKNOWN", weight=0.9),
            MockMatchResult(MockSkill("Docker"), "UNKNOWN", weight=0.5)
        ]
        self.extracted_text = "John Doe developer experience 3 years."

def test_estimator_formulas():
    # Skills weight = 50%, Experience = 25%, Education = 15%, Projects = 10%
    assert estimate_missing_skill_gain(1.0) == 50.0
    assert estimate_missing_skill_gain(0.1) == 5.0
    
    assert estimate_experience_gain(5.0) == 2.5 # 1 yr gain is (1/10)*25
    assert estimate_education_gain("Bachelor") == 3.0 # Gain to Master: 20 * 0.15 = 3.0
    assert estimate_project_gain(3) == 2.0 # 1 project gain: (1/5)*10 = 2.0

def test_heuristics_generation():
    event = MockScoredEvent()
    recs = generate_heuristics_recommendations(event)
    
    # Verify missing skills recommendations
    skills_recs = [r for r in recs if r.category == "Skills"]
    assert len(skills_recs) == 2
    assert skills_recs[0].title == "Showcase Skill: FastAPI"
    assert skills_recs[0].priority == "CRITICAL"  # weight 0.9 >= 0.8
    assert skills_recs[0].estimated_score_gain == 45.0 # 0.9 * 50
    assert skills_recs[0].source == "SEMANTIC"

    assert skills_recs[1].title == "Showcase Skill: Docker"
    assert skills_recs[1].priority == "HIGH"  # weight 0.5 >= 0.4
    assert skills_recs[1].estimated_score_gain == 25.0 # 0.5 * 50

    # Verify experience recommendation
    exp_recs = [r for r in recs if r.category == "Experience"]
    assert len(exp_recs) == 1
    assert exp_recs[0].title == "Highlight Professional Experience"
    assert exp_recs[0].priority == "HIGH" # score 40% < 70%

    # Verify projects recommendation
    proj_recs = [r for r in recs if r.category == "Projects"]
    assert len(proj_recs) == 1
    assert proj_recs[0].title == "Showcase More Technical Projects"
    assert proj_recs[0].priority == "MEDIUM"

def test_prioritizer_sorting():
    recs = [
        Recommendation(id="r1", title="Low Priority", description="", priority="LOW", category="General", reason="", source="RULE", estimated_score_gain=2.0, confidence=1.0),
        Recommendation(id="r2", title="Critical Priority", description="", priority="CRITICAL", category="General", reason="", source="RULE", estimated_score_gain=10.0, confidence=1.0),
        Recommendation(id="r3", title="High Priority", description="", priority="HIGH", category="General", reason="", source="RULE", estimated_score_gain=25.0, confidence=1.0),
        Recommendation(id="r4", title="Critical Priority Low Gain", description="", priority="CRITICAL", category="General", reason="", source="RULE", estimated_score_gain=5.0, confidence=1.0)
    ]
    
    sorted_recs = prioritize_recommendations(recs)
    assert len(sorted_recs) == 4
    # Expected order: Critical (10.0) -> Critical (5.0) -> High (25.0) -> Low (2.0)
    assert sorted_recs[0].id == "r2"
    assert sorted_recs[1].id == "r4"
    assert sorted_recs[2].id == "r3"
    assert sorted_recs[3].id == "r1"

def test_llm_enhancer_fallback():
    # Verify that without API keys in environment, enhancer fallback works and returns recommendations list as-is
    import os
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
        
    recs = [
        Recommendation(id="r1", title="Deterministic Title", description="Deterministic Description", priority="HIGH", category="Skills", reason="", source="RULE", estimated_score_gain=5.0, confidence=1.0)
    ]
    enhanced = enhance_recommendations_with_llm(recs)
    assert len(enhanced) == 1
    assert enhanced[0].title == "Deterministic Title"
    assert enhanced[0].description == "Deterministic Description"
    assert enhanced[0].source == "RULE"

def test_pipeline_integration_recommendations():
    from backend.services.pipeline import (
        ResumeTextExtractionStage,
        SkillExtractionStage,
        SemanticMatchingStage,
        ScoringStage,
        ExplanationBuildingStage,
        RecommendationBuildingStage,
        ResumeExtractedEvent
    )
    
    extract_stage = ResumeTextExtractionStage()
    skills_stage = SkillExtractionStage()
    match_stage = SemanticMatchingStage()
    scoring_stage = ScoringStage()
    explanation_stage = ExplanationBuildingStage()
    rec_stage = RecommendationBuildingStage()

    raw_text = "Jane Smith Skills: Python Education: PhD Experience: 8 years. Projects: 6 projects."
    event = ResumeExtractedEvent(
        filename="resume_test.txt",
        content_bytes=raw_text.encode("utf-8"),
        job_description="Need Python and React.",
        clean_jd="need python react"
    )
    
    res_ext = extract_stage.execute(event)
    res_skills = skills_stage.execute(res_ext)
    res_match = match_stage.execute(res_skills)
    res_score = scoring_stage.execute(res_match)
    res_explanation = explanation_stage.execute(res_score)
    res_recommendation = rec_stage.execute(res_explanation)
    
    assert res_recommendation.status == "success"
    meta = res_explanation.analysis_metadata
    assert "recommendations" in meta
    assert "list" in meta["recommendations"]
    assert "generated_at" in meta["recommendations"]
    assert meta["recommendations"]["engine_version"] == "1.0.0"
    
    # We should have a recommendation for missing React skill
    recs_list = meta["recommendations"]["list"]
    assert len(recs_list) > 0
    skills_recs = [r for r in recs_list if r["category"] == "Skills"]
    assert len(skills_recs) > 0
    assert any("React" in r["title"] for r in skills_recs)

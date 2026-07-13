import pytest
from backend.services.xai.models import ScoreComponent, Evidence
from backend.services.xai.engine import XaiEngine
from backend.services.xai.builder import build_score_components
from backend.services.xai.evidence import (
    generate_skills_evidence,
    generate_experience_evidence,
    generate_education_evidence,
    generate_projects_evidence,
    generate_document_similarity_evidence
)

# Mock classes for testing
class MockSkill:
    def __init__(self, canonical_name, category="Language", technology_family="General"):
        self.canonical_name = canonical_name
        self.category = category
        self.technology_family = technology_family

class MockMatchResult:
    def __init__(self, required_skill, candidate_skill, match_type, confidence=1.0, weight=1.0, reason=""):
        self.required_skill = required_skill
        self.candidate_skill = candidate_skill
        self.match_type = match_type
        self.confidence = confidence
        self.weight = weight
        self.reason = reason

class MockScoredEvent:
    def __init__(self):
        self.skill_score = 80.0
        self.experience_score = 50.0
        self.education_score = 60.0
        self.projects_score = 40.0
        self.similarity_score = 67.0
        self.candidate_experience = 4
        self.candidate_internships = 2
        self.candidate_education = "Bachelor"
        self.candidate_projects = 2

def test_evidence_generation():
    # 1. Test Skills evidence
    req = MockSkill("Python")
    cand = MockSkill("Python")
    match_results = [
        MockMatchResult(req, cand, "EXACT"),
        MockMatchResult(MockSkill("FastAPI"), MockSkill("Flask"), "HIERARCHICAL", confidence=0.75),
        MockMatchResult(MockSkill("Java"), MockSkill("Java"), "UNKNOWN", confidence=0.0)
    ]
    
    skills_evidence = generate_skills_evidence(match_results)
    assert len(skills_evidence) == 3
    assert skills_evidence[0].type == "exact_match"
    assert skills_evidence[0].importance == "high"
    assert skills_evidence[1].type == "hierarchical_match"
    assert skills_evidence[1].importance == "medium"
    assert skills_evidence[2].type == "unmatched"
    assert skills_evidence[2].importance == "low"

    # 2. Test Experience evidence
    exp_evidence = generate_experience_evidence(years=5, internships=2)
    assert len(exp_evidence) == 1
    assert exp_evidence[0].type == "experience_record"
    assert "5 years of professional experience" in exp_evidence[0].description
    assert "2 relevant internship" in exp_evidence[0].description
    
    # 3. Test Education evidence
    edu_evidence = generate_education_evidence("Master")
    assert len(edu_evidence) == 1
    assert edu_evidence[0].type == "education_level"
    assert "Master's degree" in edu_evidence[0].description

    # 4. Test Projects evidence
    proj_evidence = generate_projects_evidence(3)
    assert len(proj_evidence) == 1
    assert proj_evidence[0].type == "project_count"
    assert "3 technical projects" in proj_evidence[0].description

    # 5. Test Document Similarity evidence
    sim_evidence = generate_document_similarity_evidence(75.5)
    assert len(sim_evidence) == 1
    assert sim_evidence[0].type == "document_similarity"
    assert "75.5%" in sim_evidence[0].description

def test_builder_and_engine():
    event = MockScoredEvent()
    req = MockSkill("Python")
    cand = MockSkill("Python")
    match_results = [MockMatchResult(req, cand, "EXACT")]
    
    components = build_score_components(
        scoring_event=event,
        match_results=match_results,
        doc_similarity_percentage=75.0
    )
    
    assert len(components) == 6
    names = [c.name for c in components]
    assert "Technical Skills" in names
    assert "Work Experience" in names
    assert "Education" in names
    assert "Projects" in names
    assert "Document Similarity" in names
    assert "Overall Score" in names
    
    # Verify status resolution
    skills_comp = next(c for c in components if c.name == "Technical Skills")
    assert skills_comp.status == "met"  # raw_score 80 >= 80
    
    # Run Explanation Engine
    engine = XaiEngine()
    explanations = engine.generate_explanations(components)
    
    assert "skills" in explanations
    assert "experience" in explanations
    assert "education" in explanations
    assert "projects" in explanations
    assert "document_similarity" in explanations
    assert "overall" in explanations
    
    # Verify multi-level explanations
    skills_expl = explanations["skills"]
    assert "summary" in skills_expl
    assert "detailed" in skills_expl
    assert "technical" in skills_expl
    
    # Exclude plain strings checks - they are structured objects in serialization dict form
    assert isinstance(skills_expl["summary"]["why_awarded"], str)
    assert len(skills_expl["summary"]["supporting_evidence"]) == 1
    assert skills_expl["summary"]["supporting_evidence"][0]["type"] == "exact_match"

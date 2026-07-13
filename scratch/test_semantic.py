import pytest
from backend.services.skills.extractor import SkillExtractor
from backend.services.semantic.matcher import SemanticMatcher
from backend.services.semantic.scorer import SemanticScorer
from backend.services.semantic.resolver import resolve_relationship
from backend.services.screening_service import screen_resumes
from backend.services.skills.loader import get_skills_loader

def test_relationship_resolution():
    skills = get_skills_loader()
    
    # 1. EXACT match
    python_skill = next(s for s in skills if s.id == "python")
    assert python_skill is not None
    m_type, conf, weight, reason = resolve_relationship(python_skill, python_skill)
    assert m_type == "EXACT"
    assert weight == 1.0
    
    # 2. ALIAS match
    postgres_skill = next(s for s in skills if s.id == "postgresql")
    assert postgres_skill is not None
    # Let's create a temp Skill representation of "Postgres" (which is an alias of PostgreSQL)
    from backend.services.skills.models import Skill
    postgres_alias = Skill(
        id="postgres",
        canonical_name="Postgres",
        aliases=[],
        abbreviations=[],
        category="Databases",
        subcategory="Relational Databases",
        technology_family="Data Engineering"
    )
    m_type, conf, weight, reason = resolve_relationship(postgres_skill, postgres_alias)
    assert m_type == "ALIAS"
    assert weight == 0.95

    # 3. ABBREVIATION match
    llm_skill = next(s for s in skills if s.id == "large_language_models")
    llm_abbr = Skill(
        id="llm",
        canonical_name="LLM",
        aliases=[],
        abbreviations=[],
        category="Machine Learning",
        subcategory="Deep Learning",
        technology_family="Artificial Intelligence"
    )
    m_type, conf, weight, reason = resolve_relationship(llm_skill, llm_abbr)
    assert m_type == "ABBREVIATION"
    assert weight == 0.90

    # 4. HIERARCHICAL match
    fastapi_skill = next(s for s in skills if s.id == "fastapi")
    flask_skill = next(s for s in skills if s.id == "flask")
    assert fastapi_skill is not None
    assert flask_skill is not None
    m_type, conf, weight, reason = resolve_relationship(fastapi_skill, flask_skill)
    assert m_type == "HIERARCHICAL"
    assert weight == 0.75

    # 5. TECHNOLOGY_FAMILY match
    backend_family = next(s for s in skills if s.id == "backend_development")
    assert backend_family is not None
    m_type, conf, weight, reason = resolve_relationship(fastapi_skill, backend_family)
    assert m_type == "TECHNOLOGY_FAMILY"
    assert weight == 0.60

def test_semantic_matching_engine():
    extractor = SkillExtractor()
    required = extractor.extract("We need Python, FastAPI, and PostgreSQL")
    candidate = extractor.extract("I have python, Flask, and Postgres")
    
    # Required: Python, FastAPI, PostgreSQL
    # Candidate: python (exact), Flask (hierarchical sibling of FastAPI), Postgres (alias of PostgreSQL)
    matcher = SemanticMatcher()
    results = matcher.match_skills(required, candidate)
    
    # We should have 3 matches
    assert len(results) == 3
    
    # Match 1: Python matches python (EXACT)
    python_match = next(r for r in results if r.required_skill.id == "python")
    assert python_match.match_type == "EXACT"
    assert python_match.weight == 1.00
    
    # Match 2: FastAPI matches Flask (HIERARCHICAL)
    fastapi_match = next(r for r in results if r.required_skill.id == "fastapi")
    assert fastapi_match.match_type == "HIERARCHICAL"
    assert fastapi_match.weight == 0.75
    
    # Match 3: PostgreSQL matches Postgres (EXACT due to normalization mapping both to PostgreSQL Skill)
    postgres_match = next(r for r in results if r.required_skill.id == "postgresql")
    assert postgres_match.match_type == "EXACT"
    assert postgres_match.weight == 1.00

def test_semantic_scorer():
    extractor = SkillExtractor()
    required = extractor.extract("Python, FastAPI, SQL")
    candidate = extractor.extract("Python, Flask")  # Python (EXACT: 1.0), FastAPI matches Flask (HIERARCHICAL: 0.75), SQL has no match (UNKNOWN: 0.0)
    
    matcher = SemanticMatcher()
    scorer = SemanticScorer()
    
    results = matcher.match_skills(required, candidate)
    breakdown = scorer.calculate_score(results)
    
    # Overall score = (1.0 + 0.75 + 0.0) / 3 = 0.5833 * 100 = 58.33%
    assert breakdown["overall"] == pytest.approx(58.33, 0.01)

def test_screening_service_integration():
    import anyio
    
    # Create valid minimal PDF content with Helvetica font mapping for PyPDF2 text extraction
    pdf_content = b'''%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> >>
endobj
4 0 obj
<< /Length 70 >>
stream
BT
/F1 12 Tf
70 700 Td
(John Doe Skills: Python, Flask Education: Bachelor Experience: 0) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000257 00000 n
trailer
<< /Size 5 /Root 1 0 R >>
startxref
348
%%EOF
'''

    async def run_test():
        job_description = "We need a Software Engineer skilled in Python, FastAPI, and SQL."
        resumes_data = [
            {
                "filename": "candidate_1.pdf",
                "content": pdf_content
            }
        ]
        return await screen_resumes(job_description, resumes_data)
        
    results = anyio.run(run_test)
    assert "results" in results
    cand_result = results["results"][0]
    
    # Skills match:
    # Python -> Python (EXACT: 1.00)
    # FastAPI -> Flask (HIERARCHICAL: 0.75)
    # SQL -> None (UNKNOWN: 0.00)
    # Semantic Score: (1.0 + 0.75 + 0.0)/3 = 58.33%
    assert cand_result["semantic_score"] == pytest.approx(58.33, 0.01)
    assert cand_result["skill_score"] == pytest.approx(58.33, 0.01)
    
    # Check semantic metadata matches lists
    sem_data = cand_result["semantic_data"]
    assert len(sem_data["exact_matches"]) == 1  # Python
    assert len(sem_data["hierarchical_matches"]) == 1  # Flask
    assert len(sem_data["alias_matches"]) == 0
    assert len(sem_data["family_matches"]) == 0

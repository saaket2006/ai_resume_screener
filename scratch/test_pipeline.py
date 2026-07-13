import pytest
import anyio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from backend.database.database import Base
from backend.services.pipeline import (
    ResumeExtractedEvent,
    ResumeTextExtractionStage,
    SkillExtractionStage,
    SemanticMatchingStage,
    ScoringStage,
    ExplanationBuildingStage,
    PersistenceStage,
    AnalysisPipeline
)
from backend.models.models import User, JobDescription, Resume, ScanResult
from backend.models.enums import UserRole

from backend.config import settings
settings.ALLOWED_EXTENSIONS.add(".txt")

# Use an in-memory SQLite database for test persistence
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create test candidate and recruiter users
    cand = User(email="test_cand@screener.com", hashed_password="pw", profile_completed=True, role=UserRole.CANDIDATE)
    rec = User(email="test_rec@screener.com", hashed_password="pw", profile_completed=True, role=UserRole.RECRUITER)
    db.add_all([cand, rec])
    db.commit()
    
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_pipeline_extraction_stage():
    stage = ResumeTextExtractionStage()
    
    # 1. Valid PDF format
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
    event = ResumeExtractedEvent(
        filename="resume.pdf",
        content_bytes=pdf_content,
        job_description="Need Python and FastAPI.",
        clean_jd="need python and fastapi"
    )
    res = stage.execute(event)
    assert res.status == "success"
    assert "John Doe" in res.raw_text
    
    # 2. Unsupported extension
    event_unsupported = ResumeExtractedEvent(
        filename="resume.png",
        content_bytes=b"fakebytes",
        job_description="Need Python.",
        clean_jd="need python"
    )
    res_unsupported = stage.execute(event_unsupported)
    assert res_unsupported.status == "error"
    assert res_unsupported.error_message == "Unsupported/Invalid File"

def test_pipeline_skill_extraction_stage():
    extract_stage = ResumeTextExtractionStage()
    skills_stage = SkillExtractionStage()
    
    # Text contains Python, Flask, which will extract properly
    raw_text = "John Doe Skills: Python, Flask Education: Bachelor Experience: 5 years."
    event = ResumeExtractedEvent(
        filename="resume.txt",
        content_bytes=raw_text.encode("utf-8"),
        job_description="Need Python and FastAPI.",
        clean_jd="need python and fastapi"
    )
    
    # Run Stage 1 & 2
    res_ext = extract_stage.execute(event)
    res_skills = skills_stage.execute(res_ext)
    
    assert res_skills.status == "success"
    # Verify we extracted Python as a JD skill
    assert "python" in res_skills.jd_skills_names
    # Verify candidate has python
    cand_skill_ids = [s.id for s in res_skills.candidate_skills_objs]
    assert "python" in cand_skill_ids

def test_pipeline_semantic_matching_stage():
    extract_stage = ResumeTextExtractionStage()
    skills_stage = SkillExtractionStage()
    match_stage = SemanticMatchingStage()
    
    raw_text = "John Doe Skills: Python, Flask"
    event = ResumeExtractedEvent(
        filename="resume.txt",
        content_bytes=raw_text.encode("utf-8"),
        job_description="Need Python, FastAPI, and SQL.",
        clean_jd="need python fastapi sql"
    )
    
    res_ext = extract_stage.execute(event)
    res_skills = skills_stage.execute(res_ext)
    res_match = match_stage.execute(res_skills)
    
    assert res_match.status == "success"
    # Python (EXACT: 1.0), FastAPI matches Flask (HIERARCHICAL: 0.75), SQL (UNKNOWN: 0.0)
    # Expected: exact_matches should contain Python, hierarchical_matches should contain Flask/FastAPI
    exact_req = [item["required"] for item in res_match.semantic_metadata_payload["exact_matches"]]
    hierarchical_req = [item["required"] for item in res_match.semantic_metadata_payload["hierarchical_matches"]]
    
    assert "Python" in exact_req
    assert "FastAPI" in hierarchical_req
    # Average score = (1.0 + 0.75 + 0.0) / 3 = 0.5833 * 100 = 58.33%
    assert res_match.semantic_metadata_payload["semantic_score"] == pytest.approx(58.33, 0.01)

def test_pipeline_scoring_and_explanations():
    extract_stage = ResumeTextExtractionStage()
    skills_stage = SkillExtractionStage()
    match_stage = SemanticMatchingStage()
    scoring_stage = ScoringStage()
    explanation_stage = ExplanationBuildingStage()
    
    raw_text = "John Doe Skills: Python, Flask Education: Master Experience: 3 years."
    event = ResumeExtractedEvent(
        filename="resume.txt",
        content_bytes=raw_text.encode("utf-8"),
        job_description="Need Python and FastAPI.",
        clean_jd="need python fastapi"
    )
    
    res_ext = extract_stage.execute(event)
    res_skills = skills_stage.execute(res_ext)
    res_match = match_stage.execute(res_skills)
    res_score = scoring_stage.execute(res_match)
    res_explanation = explanation_stage.execute(res_score)
    
    assert res_explanation.status == "success"
    assert res_explanation.analysis_metadata["xai"]["enabled"] is True
    assert "skills_summary" in res_explanation.xai_explanations
    assert "experience_summary" in res_explanation.xai_explanations
    assert "Master" in res_explanation.xai_explanations["education_summary"]

def test_pipeline_persistence_stage(setup_db):
    db = setup_db
    
    # Setup test JD
    cand_user = db.query(User).filter(User.email == "test_cand@screener.com").first()
    rec_user = db.query(User).filter(User.email == "test_rec@screener.com").first()
    
    jd = JobDescription(owner_id=rec_user.id, title="Software Engineer", description="Need Python.")
    db.add(jd)
    db.flush()
    
    pipeline = AnalysisPipeline()
    raw_text = "John Doe Skills: Python Education: Bachelor Experience: 2 years."
    
    explanation_result = pipeline.run_analysis(
        filename="resume_save.txt",
        content_bytes=raw_text.encode("utf-8"),
        job_description="Need Python.",
        clean_jd="need python"
    )
    
    assert explanation_result.status == "success"
    
    # Save via PersistenceStage
    persist_stage = PersistenceStage(db)
    persistence_result = persist_stage.execute(
        explanation_result,
        candidate_id=cand_user.id,
        version=1,
        label="Test Pipeline Version",
        label_source="SYSTEM",
        job_description_id=jd.id,
        ats_score=85.5,
        elapsed_ms=120
    )
    
    assert persistence_result.status == "success"
    db.commit()
    
    # Query database and verify persistence details
    resume_record = db.query(Resume).filter(Resume.id == persistence_result.resume_id).first()
    assert resume_record is not None
    assert resume_record.original_filename == "resume_save.txt"
    assert resume_record.label == "Test Pipeline Version"
    
    scan_record = db.query(ScanResult).filter(ScanResult.id == persistence_result.scan_result_id).first()
    assert scan_record is not None
    assert scan_record.ats_score == 85.5
    assert scan_record.analysis_metadata["xai"]["enabled"] is True
    assert "Python" in scan_record.analysis_metadata["xai"]["explanations"]["skills"]["summary"]["why_awarded"]

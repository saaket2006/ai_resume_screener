import time
import os
import sys
import unittest.mock as mock

os.environ["DATABASE_URL"] = "postgres://fake:fake@fake:5432/fake"

with mock.patch("sqlalchemy.create_engine") as mock_engine:
    from backend.database.database import Base
    from backend.models.models import JobDescription, Resume, ScanResult, User
    from backend.services.pipeline import PersistenceStage, AnalysisContext
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def mock_pipeline_ctx(score=50.0):
    ctx = AnalysisContext("test_id")
    class MockExtraction:
        raw_text = "test raw text"
        filename = "test.pdf"
        file_ext = "pdf"
    class MockSkills:
        extraction = MockExtraction()
    class MockMatching:
        skills = MockSkills()
    class MockScoring:
        matching = MockMatching()
        similarity_score = score
        candidate_name = "Test"
        candidate_email = "test@example.com"
        candidate_phone = "123"
        candidate_linkedin = ""
    class MockExplanation:
        scoring = MockScoring()
        analysis_metadata = {"score": {}, "engine": {}}
    class MockRec:
        explanation = MockExplanation()
        error_message = None
        status = "success"
    class MockEvent:
        status = "success"
        explanation = MockExplanation()
        recommendation = MockRec()
        error_message = None
    ctx.event = MockEvent()
    ctx.metrics = {}
    return ctx

def run_optimized(num_candidates=100):
    db = TestingSessionLocal()
    jd = JobDescription(id=1, owner_id=1, title="Test", description="Test JD")
    user = User(id=1, email="test@example.com", hashed_password="test")
    db.add(user)
    db.flush()
    jd.owner_id = user.id
    db.add(jd)
    db.flush()

    candidates = []
    for i in range(num_candidates):
        candidates.append({
            "email": "test@example.com",
            "name": "Test User",
            "filename": f"test_{i}.pdf",
            "pipeline_context": mock_pipeline_ctx(score=i * 0.5),
            "similarity_score": i * 0.5
        })

    results = {"results": candidates}

    # OPTIMIZED
    start = time.time()
    persist_stage = PersistenceStage(db)
    batch_args = []

    for cand in results.get("results", []):
        pipeline_ctx = cand["pipeline_context"]
        batch_args.append({
            "arg": pipeline_ctx,
            "kwargs": {
                "candidate_id": None,
                "version": 1,
                "label": None,
                "label_source": "SYSTEM",
                "job_description_id": jd.id,
                "ats_score": cand["similarity_score"],
                "elapsed_ms": 0
            }
        })

    if batch_args:
        batch_results = persist_stage.execute_batch(batch_args)

    db.commit()
    end = time.time()
    optimized_time = end - start
    print(f"Optimized for {num_candidates} resumes: {optimized_time:.4f} seconds")

    db.close()

if __name__ == "__main__":
    run_optimized(1000)

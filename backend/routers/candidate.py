import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.dependencies.auth_deps import require_candidate
from backend.database.database import get_db
from backend.models.models import User, Resume, JobDescription, ScanResult
from backend.services.document_service import extract_text as parse_document_text
from backend.services.screening_service import screen_resumes

logger = logging.getLogger("resume_screener")

router = APIRouter(prefix="/candidate", tags=["candidate"])

@router.get("/status")
def candidate_status():
    """Endpoint for checking candidate service status."""
    return {"status": "candidate service is active"}

@router.post("/process")
async def process_candidate_resume(
    job_description: str = Form(...),
    resume: UploadFile = File(...),
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    """
    Evaluates a candidate's resume against a pasted job description using the shared ATS engine.
    Persists the resume parsed text, job description, and scan results in database.
    """
    logger.info("Candidate endpoint called by user: %s", current_user.email)

    if not job_description:
        raise HTTPException(status_code=400, detail="Job description is required")
        
    if not resume or not resume.filename:
        raise HTTPException(status_code=400, detail="Resume file is required")

    filename = resume.filename
    try:
        content = await resume.read()
    except Exception as e:
        logger.error("Failed to read candidate resume file: %s", e)
        raise HTTPException(status_code=400, detail="Unreadable resume file")

    try:
        # 1. Parse/Extract text from resume
        raw_text = parse_document_text(content, filename)
    except ValueError as e:
        logger.error("Resume extraction failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e))

    try:
        # 2. Run screening using existing ATS service
        resumes_data = [{"filename": filename, "content": content}]
        results = await screen_resumes(job_description, resumes_data)
        
        # Verify result exists
        if not results.get("results"):
            raise HTTPException(status_code=400, detail="Parsing failed to generate valid results")
            
        candidate_result = results["results"][0]

        # 3. Create database records
        # Save Job Description
        jd_model = JobDescription(
            recruiter_id=None,  # Nullable since candidate-submitted
            title=job_description[:50] + ("..." if len(job_description) > 50 else ""),
            description=job_description
        )
        db.add(jd_model)
        db.flush()

        # Save Resume
        resume_model = Resume(
            candidate_id=current_user.id,
            extracted_text=raw_text,
            version=1
        )
        db.add(resume_model)
        db.flush()

        # Save Scan Result
        scan_result = ScanResult(
            resume_id=resume_model.id,
            job_description_id=jd_model.id,
            ats_score=candidate_result["similarity_score"]
        )
        db.add(scan_result)
        db.commit()

        logger.info("Candidate resume analysis persisted successfully for ScanResult ID %d", scan_result.id)
        return results

    except HTTPException:
        db.rollback()
        raise
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.exception("Error during candidate screening:")
        raise HTTPException(status_code=500, detail="Internal server error during screening")

@router.get("/stats")
def get_candidate_stats(
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    """
    Retrieves latest ATS score details for candidate dashboard metrics.
    """
    logger.info("Candidate stats requested for user: %s", current_user.email)

    latest_scan = (
        db.query(ScanResult)
        .join(Resume)
        .filter(Resume.candidate_id == current_user.id)
        .order_by(ScanResult.created_at.desc())
        .first()
    )

    if not latest_scan:
        return {"latest_ats_score": None}

    return {
        "latest_ats_score": latest_scan.ats_score,
        "timestamp": latest_scan.created_at.isoformat()
    }

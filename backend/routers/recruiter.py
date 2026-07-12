from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request, Depends
from typing import List
import logging
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.services.screening_service import screen_resumes
from backend.limiter import limiter
from backend.dependencies.auth_deps import require_recruiter
from backend.database.database import get_db
from backend.models.models import User, JobDescription, Resume, ScanResult

logger = logging.getLogger("resume_screener")

router = APIRouter(prefix="/recruiter", tags=["recruiter"])

@router.post("/process")
@limiter.limit("5/minute")
async def process_resumes(
    request: Request,
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...),
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Screens uploaded resume files against a job description.
    Enforces authentication and recruiter role verification.
    Persists screening results inside the database for dashboard statistics.
    """
    logger.info("Recruiter endpoint called by user: %s", current_user.email)
    
    if not job_description:
        raise HTTPException(status_code=400, detail="Job description is required")
        
    if not resumes:
        raise HTTPException(status_code=400, detail="At least one resume must be uploaded")
        
    resumes_data = []
    for resume in resumes:
        filename = resume.filename
        if not filename:
            continue
        try:
            content = await resume.read()
            resumes_data.append({
                "filename": filename,
                "content": content
            })
        except Exception as e:
            logger.error("Failed to read uploaded resume file '%s': %s", filename, e)
            
    try:
        results = await screen_resumes(job_description, resumes_data)
        
        # Save Job Description
        jd_model = JobDescription(
            recruiter_id=current_user.id,
            title=job_description[:50] + ("..." if len(job_description) > 50 else ""),
            description=job_description
        )
        db.add(jd_model)
        db.flush()  # Obtain jd_model.id
        
        # Save each parsed candidate resume and scan result
        for cand in results.get("results", []):
            # Skip invalid/error files from saving
            if cand.get("email") == "N/A" and cand.get("name") in ("Unsupported/Invalid File", "File Too Large (>5MB)"):
                continue
                
            resume_model = Resume(
                candidate_id=None,  # Nullable since external candidate
                extracted_text=f"Resume file: {cand['filename']}",
                version=1
            )
            db.add(resume_model)
            db.flush()  # Obtain resume_model.id
            
            scan_result = ScanResult(
                resume_id=resume_model.id,
                job_description_id=jd_model.id,
                ats_score=cand["similarity_score"]
            )
            db.add(scan_result)
            
        db.commit()
        logger.info("Screening persisted successfully for job description ID %d", jd_model.id)
        
        return results
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.exception("Error during screening:")
        raise HTTPException(status_code=500, detail="Internal server error during screening")

@router.get("/stats")
def get_recruiter_stats(
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Retrieves the simple dashboard statistics for the authenticated recruiter:
    - Total Candidates Screened
    - Average ATS Score
    """
    logger.info("Recruiter stats requested for user: %s", current_user.email)
    
    total_candidates = db.query(ScanResult).join(JobDescription).filter(JobDescription.recruiter_id == current_user.id).count()
    
    avg_score_res = db.query(func.avg(ScanResult.ats_score)).join(JobDescription).filter(JobDescription.recruiter_id == current_user.id).scalar()
    
    avg_score = round(float(avg_score_res), 1) if avg_score_res is not None else 0.0
    
    return {
        "total_candidates_screened": total_candidates,
        "average_ats_score": avg_score
    }

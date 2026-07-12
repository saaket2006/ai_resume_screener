import logging
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.dependencies.auth_deps import require_candidate
from backend.database.database import get_db
from backend.models.models import User, Resume, JobDescription, ScanResult, CandidateProfile
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
    label: Optional[str] = Form(None),
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    """
    Evaluates a candidate's resume against a pasted job description using the shared ATS engine.
    Persists the resume parsed text, job description, and scan results in database.
    Supports resume versioning, editable labels, and analysis snapshotting.
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

        # Determine version
        profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
        if profile:
            profile.resume_version_counter += 1
            version = profile.resume_version_counter
        else:
            # Fallback if profile doesn't exist
            version = 1

        # Default label if not provided
        if not label or not label.strip():
            label_val = f"Version {version}"
        else:
            label_val = label.strip()

        # 3. Create database records
        # Save Job Description
        jd_model = JobDescription(
            owner_id=current_user.id,
            title=job_description[:50] + ("..." if len(job_description) > 50 else ""),
            description=job_description
        )
        db.add(jd_model)
        db.flush()

        # Save Resume
        file_ext = filename.split(".")[-1].lower() if "." in filename else "unknown"
        resume_model = Resume(
            candidate_id=current_user.id,
            extracted_text=raw_text,
            original_filename=filename,
            file_type=file_ext,
            version=version,
            label=label_val
        )
        db.add(resume_model)
        db.flush()

        # Build analysis metadata snapshot
        analysis_metadata = {
            "matched_skills": candidate_result["matched_skills"],
            "missing_skills": candidate_result["missing_skills"],
            "extracted_skills": candidate_result["matched_skills"],  # Candidate's own skills
            "candidate_name": candidate_result["name"],
            "email": candidate_result["email"],
            "phone": candidate_result["phone"],
            "linkedin": candidate_result.get("linkedin", "Not Provided"),
            "github": candidate_result.get("github", "Not Provided"),
            "experience": candidate_result.get("experience", 0),
            "education": candidate_result.get("education", "None"),
            "projects": candidate_result.get("projects", 0),
            "skill_score": candidate_result.get("skill_score", 0.0),
            "experience_score": candidate_result.get("experience_score", 0.0),
            "education_score": candidate_result.get("education_score", 0.0),
            "projects_score": candidate_result.get("projects_score", 0.0)
        }

        # Save Scan Result
        scan_result = ScanResult(
            resume_id=resume_model.id,
            job_description_id=jd_model.id,
            ats_score=candidate_result["similarity_score"],
            analysis_metadata=analysis_metadata
        )
        db.add(scan_result)
        db.commit()

        logger.info("Candidate resume analysis persisted successfully for ScanResult ID %d", scan_result.id)
        
        # Include resume versioning details in the return result
        candidate_result["version"] = version
        candidate_result["label"] = label_val
        candidate_result["resume_id"] = resume_model.id
        candidate_result["uploaded_at"] = resume_model.uploaded_at.isoformat()

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

@router.get("/resumes")
def get_candidate_resumes(
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    """
    Retrieves all resume versions uploaded by the candidate, ordered by newest first.
    """
    logger.info("Candidate resumes list requested for user: %s", current_user.email)
    resumes = (
        db.query(Resume)
        .filter(Resume.candidate_id == current_user.id)
        .order_by(Resume.version.desc())
        .all()
    )

    response_data = []
    for r in resumes:
        score = None
        jd_title = None
        jd_summary = None
        if r.scan_results:
            scan = r.scan_results[0]
            score = scan.ats_score
            if scan.job_description:
                jd_title = scan.job_description.title
                jd_summary = scan.job_description.description[:100] + ("..." if len(scan.job_description.description) > 100 else "")
        response_data.append({
            "id": r.id,
            "version": r.version,
            "original_filename": r.original_filename,
            "label": r.label,
            "uploaded_at": r.uploaded_at.isoformat(),
            "ats_score": score,
            "job_description_title": jd_title,
            "job_description_summary": jd_summary
        })

    return response_data

@router.get("/resumes/{resume_id}")
def get_candidate_resume_details(
    resume_id: int,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    """
    Retrieves full historical snapshot details for a specific resume version.
    """
    logger.info("Candidate resume details requested for resume ID %d, user: %s", resume_id, current_user.email)
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.candidate_id == current_user.id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume version not found")

    scan = resume.scan_results[0] if resume.scan_results else None
    score = scan.ats_score if scan else 0.0
    meta = scan.analysis_metadata if scan else {}

    return {
        "id": resume.id,
        "version": resume.version,
        "label": resume.label,
        "original_filename": resume.original_filename,
        "file_type": resume.file_type,
        "uploaded_at": resume.uploaded_at.isoformat(),
        "ats_score": score,
        "job_description": {
            "title": scan.job_description.title if scan and scan.job_description else "",
            "description": scan.job_description.description if scan and scan.job_description else ""
        } if scan else None,
        "extracted_skills": meta.get("extracted_skills", []),
        "matched_skills": meta.get("matched_skills", []),
        "missing_skills": meta.get("missing_skills", []),
        "candidate_details": {
            "name": meta.get("candidate_name", "N/A"),
            "email": meta.get("email", "N/A"),
            "phone": meta.get("phone", "N/A"),
            "linkedin": meta.get("linkedin", "N/A"),
            "github": meta.get("github", "N/A"),
            "experience": meta.get("experience", 0),
            "education": meta.get("education", "N/A"),
            "projects": meta.get("projects", 0),
            "skill_score": meta.get("skill_score", 0.0),
            "experience_score": meta.get("experience_score", 0.0),
            "education_score": meta.get("education_score", 0.0),
            "projects_score": meta.get("projects_score", 0.0)
        }
    }

@router.delete("/resumes/{resume_id}")
def delete_candidate_resume(
    resume_id: int,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    """
    Deletes a single resume version. Deleting one version does not affect other versions.
    """
    logger.info("Candidate resume deletion requested for resume ID %d, user: %s", resume_id, current_user.email)
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.candidate_id == current_user.id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume version not found")

    db.delete(resume)
    db.commit()
    return {"message": "Resume version deleted successfully"}

@router.put("/resumes/{resume_id}/label")
def update_candidate_resume_label(
    resume_id: int,
    payload: dict,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    """
    Updates the editable label of a specific resume version.
    """
    logger.info("Candidate resume label update requested for resume ID %d, user: %s", resume_id, current_user.email)
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.candidate_id == current_user.id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume version not found")

    new_label = payload.get("label")
    if not new_label or not new_label.strip():
        raise HTTPException(status_code=400, detail="Label cannot be empty")

    resume.label = new_label.strip()
    db.commit()
    return {"message": "Label updated successfully", "label": resume.label}

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
        "last_analysis_date": latest_scan.created_at.isoformat(),
        "timestamp": latest_scan.created_at.isoformat()
    }

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

from typing import Optional

@router.post("/process")
@limiter.limit("5/minute")
async def process_resumes(
    request: Request,
    job_description: Optional[str] = Form(None),
    jd_id: Optional[int] = Form(None),
    profile_id: Optional[int] = Form(None),
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
    
    # Resolve Job Description Text
    if jd_id:
        jd_model = db.query(JobDescription).filter(
            JobDescription.id == jd_id,
            JobDescription.owner_id == current_user.id
        ).first()
        if not jd_model:
            raise HTTPException(status_code=404, detail="Job description not found in your library")
        jd_text = jd_model.description
    else:
        if not job_description or not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description text is required when no jd_id is provided")
        jd_text = job_description
        # Save new Job Description into library
        jd_model = JobDescription(
            owner_id=current_user.id,
            title=job_description[:50] + ("..." if len(job_description) > 50 else ""),
            description=job_description
        )
        db.add(jd_model)
        db.flush()  # Obtain jd_model.id
        
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
        results = await screen_resumes(jd_text, resumes_data, db=db, profile_id=profile_id)
        
        # Save each parsed candidate resume and scan result
        for cand in results.get("results", []):
            # Skip invalid/error files from saving
            if cand.get("email") == "N/A" and cand.get("name") in ("Unsupported/Invalid File", "File Too Large (>5MB)"):
                continue
                
            fn = cand.get("filename", "unknown_file")
            ext = fn.split(".")[-1].lower() if "." in fn else "unknown"
            from backend.services.pipeline import PersistenceStage
            persist_stage = PersistenceStage(db)
            
            # Pass context down to persistence stage so metrics get saved
            pipeline_ctx = cand["pipeline_context"]
            
            persistence_result = persist_stage.execute(
                pipeline_ctx,
                candidate_id=None,
                version=1,
                label=None,
                label_source="SYSTEM",
                job_description_id=jd_model.id,
                ats_score=cand["similarity_score"],
                elapsed_ms=0
            )
            if persistence_result.status != "success":
                raise HTTPException(status_code=500, detail=persistence_result.error_message)
            
        db.commit()
        logger.info("Screening persisted successfully for job description ID %d", jd_model.id)
        
        for cand in results.get("results", []):
            cand.pop("pipeline_event", None)
            cand.pop("pipeline_context", None)
            
        return results
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.exception("Error during screening:")
        raise HTTPException(status_code=500, detail="Internal server error during screening")

@router.get("/profiles")
def get_scoring_profiles(
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Returns all configured and seeded scoring profiles.
    """
    from backend.models.models import ScoringProfile
    profiles = db.query(ScoringProfile).order_by(ScoringProfile.name).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "target_role": p.target_role,
            "experience_level": p.experience_level,
            "domain": p.domain,
            "weights": p.weights,
            "is_default": p.is_default
        }
        for p in profiles
    ]

# ==========================================
# JD Library CRUD Endpoints
# ==========================================

@router.get("/jobs")
def list_job_descriptions(
    include_archived: bool = False,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Retrieves all job descriptions created by the recruiter.
    """
    query = db.query(JobDescription).filter(JobDescription.owner_id == current_user.id)
    if not include_archived:
        query = query.filter(JobDescription.is_archived == False)
    jds = query.order_by(JobDescription.created_at.desc()).all()
    return [
        {
            "id": j.id,
            "title": j.title,
            "subtitle": j.subtitle,
            "description": j.description,
            "company": j.company,
            "optional_notes": j.optional_notes,
            "is_archived": j.is_archived,
            "created_at": j.created_at.isoformat()
        }
        for j in jds
    ]

@router.post("/jobs")
def create_job_description(
    title: str = Form(...),
    subtitle: Optional[str] = Form(None),
    description: str = Form(...),
    company: Optional[str] = Form(None),
    optional_notes: Optional[str] = Form(None),
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Adds a new job description to the recruiter's library.
    """
    jd = JobDescription(
        owner_id=current_user.id,
        title=title,
        subtitle=subtitle,
        description=description,
        company=company,
        optional_notes=optional_notes
    )
    db.add(jd)
    db.commit()
    return {"message": "Job description created successfully", "id": jd.id}

@router.put("/jobs/{jd_id}")
def update_job_description(
    jd_id: int,
    title: str = Form(...),
    subtitle: Optional[str] = Form(None),
    description: str = Form(...),
    company: Optional[str] = Form(None),
    optional_notes: Optional[str] = Form(None),
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Edits an existing job description in the recruiter's library.
    """
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id, JobDescription.owner_id == current_user.id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
        
    jd.title = title
    jd.subtitle = subtitle
    jd.description = description
    jd.company = company
    jd.optional_notes = optional_notes
    db.commit()
    return {"message": "Job description updated successfully"}

@router.delete("/jobs/{jd_id}")
def archive_job_description(
    jd_id: int,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Soft-deletes (archives) a job description.
    """
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id, JobDescription.owner_id == current_user.id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
        
    jd.is_archived = True
    db.commit()
    return {"message": "Job description archived successfully"}

@router.delete("/jobs/{jd_id}/delete")
def delete_job_description(
    jd_id: int,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Permanently deletes a job description and its scan results.
    """
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id, JobDescription.owner_id == current_user.id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
        
    db.delete(jd)
    db.commit()
    return {"message": "Job description and all associated results deleted permanently"}

# ==========================================
# Dashboard & Recruiter Stats Route
# ==========================================

@router.get("/stats")
def get_recruiter_stats(
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    """
    Retrieves dashboard statistics and aggregates recruiter intelligence statistics.
    """
    logger.info("Recruiter stats requested for user: %s", current_user.email)
    
    scans = db.query(ScanResult).join(JobDescription).filter(JobDescription.owner_id == current_user.id).all()
    
    total_candidates = len(scans)
    avg_score = 0.0
    if total_candidates > 0:
        avg_score = round(sum(s.ats_score for s in scans) / total_candidates, 1)
        
    # Intelligence statistics
    experience_sum = 0.0
    experience_count = 0
    education_counts = {}
    missing_skills_counts = {}
    matched_skills_counts = {}
    improvement_counts = {}
    
    for s in scans:
        meta = s.analysis_metadata or {}
        candidate_info = meta.get("candidate", {})
        
        # 1. Experience
        exp = candidate_info.get("experience")
        if exp is not None:
            try:
                experience_sum += float(exp)
                experience_count += 1
            except (ValueError, TypeError):
                pass
                
        # 2. Education
        edu = candidate_info.get("education")
        if edu:
            education_counts[edu] = education_counts.get(edu, 0) + 1
            
        # 3. Missing Skills
        skills_info = meta.get("skills", {})
        missing = skills_info.get("missing", [])
        for skill in missing:
            skill_lower = skill.strip().lower()
            if skill_lower:
                missing_skills_counts[skill_lower] = missing_skills_counts.get(skill_lower, 0) + 1
                
        # 4. Matched Skills
        matched = skills_info.get("matched", [])
        for skill in matched:
            skill_lower = skill.strip().lower()
            if skill_lower:
                matched_skills_counts[skill_lower] = matched_skills_counts.get(skill_lower, 0) + 1
                
        # 5. Recommended improvements
        recs = meta.get("recommendations", {}).get("list", [])
        for r in recs:
            title = r.get("title")
            if title:
                improvement_counts[title] = improvement_counts.get(title, 0) + 1
                
    # Format and sort aggregates
    avg_experience = round(experience_sum / experience_count, 1) if experience_count > 0 else 0.0
    
    common_missing = sorted(
        [{"skill": k, "count": v} for k, v in missing_skills_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:5]
    
    common_matched = sorted(
        [{"skill": k, "count": v} for k, v in matched_skills_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:5]
    
    top_improvements = sorted(
        [{"recommendation": k, "count": v} for k, v in improvement_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:5]
    
    most_common_edu = "None"
    if education_counts:
        most_common_edu = max(education_counts, key=education_counts.get)
        
    return {
        "total_candidates_screened": total_candidates,
        "average_ats_score": avg_score,
        "average_experience_tenure": avg_experience,
        "most_common_education_level": most_common_edu,
        "most_common_missing_skills": common_missing,
        "most_common_matched_skills": common_matched,
        "top_recommended_improvements": top_improvements,
        "education_breakdown": [{"level": k, "count": v} for k, v in education_counts.items()]
    }

import time
import logging
from typing import List, Dict
from backend.services.nlp_service import preprocess_text
from backend.services.skill_extractor import extract_skills
from backend.services.document_service import extract_text
from backend.services.info_extractor import (
    extract_name, extract_email, extract_phone, extract_linkedin,
    extract_github, extract_experience, extract_relevant_internships,
    extract_education, extract_projects
)
from backend.services.skill_expander import get_related_skills, is_skill_in_text
from backend.services.scoring_service import rank_candidates
from backend.config import settings

logger = logging.getLogger("resume_screener")

async def screen_resumes(job_description: str, resumes: List[Dict]) -> Dict:
    """
    Core business logic to screen and rank candidate resumes against a job description.
    
    resumes parameter format:
    [
        {"filename": "resume.pdf", "content": b"...bytes..."}
    ]
    """
    start_time = time.time()
    logger.info("=" * 60)
    logger.info("New screening request started: %d resume(s) uploaded", len(resumes))

    if not job_description:
        logger.warning("Screening request rejected: Job description is empty")
        raise ValueError("Job description is required")
        
    if not resumes:
        logger.warning("Screening request rejected: No resumes uploaded")
        raise ValueError("At least one resume must be uploaded")
        
    # Process Job Description
    clean_jd = preprocess_text(job_description)
    jd_skills = extract_skills(job_description)
    logger.info("JD skills extracted (%d): %s", len(jd_skills), ", ".join(jd_skills))
    
    processed_resumes = []
    
    for resume in resumes:
        filename = resume.get("filename", "unknown_file")
        contents = resume.get("content", b"")
        
        # File type validation
        if not any(filename.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
            logger.warning("Skipping '%s': Unsupported file extension", filename)
            processed_resumes.append({
                "filename": filename,
                "name": "Unsupported/Invalid File",
                "email": "N/A",
                "phone": "N/A",
                "matched_skills": [],
                "missing_skills": sorted(jd_skills)
            })
            continue
        
        # File size validation
        if len(contents) > settings.MAX_FILE_SIZE:
            logger.warning("Skipping '%s': File size (%d bytes) exceeds limit (%d bytes)", 
                           filename, len(contents), settings.MAX_FILE_SIZE)
            processed_resumes.append({
                "filename": filename,
                "name": "File Too Large (>5MB)",
                "email": "N/A",
                "phone": "N/A",
                "matched_skills": [],
                "missing_skills": sorted(jd_skills)
            })
            continue
        
        # Extract text based on file type
        try:
            raw_text = extract_text(contents, filename)
        except ValueError as e:
            logger.error("Skipping '%s': Text extraction failed: %s", filename, e)
            processed_resumes.append({
                "filename": filename,
                "name": "Unreadable File",
                "email": "N/A",
                "phone": "N/A",
                "matched_skills": [],
                "missing_skills": sorted(jd_skills)
            })
            continue
        
        # Extract candidate details
        candidate_name = extract_name(raw_text)
        candidate_email = extract_email(raw_text)
        candidate_phone = extract_phone(raw_text)
        candidate_linkedin = extract_linkedin(raw_text)
        candidate_github = extract_github(raw_text)
        candidate_experience = extract_experience(raw_text)
        candidate_internships = extract_relevant_internships(raw_text, jd_skills)
        candidate_education = extract_education(raw_text)
        candidate_projects = extract_projects(raw_text)
        
        # Preprocess text
        clean_text = preprocess_text(raw_text)
        
        # Skill matching and expansions
        raw_text_lower = raw_text.lower()
        matched = []
        missing = []
        
        for skill in jd_skills:
            related_skills, is_broad = get_related_skills(skill)
            has_exact = is_skill_in_text(skill, raw_text_lower)
            
            if is_broad and related_skills:
                found_related = []
                for rs in related_skills:
                    if is_skill_in_text(rs, raw_text_lower):
                        found_related.append(rs)
                        
                if has_exact or len(found_related) >= 1:
                    matched.append(skill)
                    matched.extend(found_related)
                else:
                    missing.append(skill)
            else:
                if has_exact:
                    matched.append(skill)
                else:
                    missing.append(skill)
                    
        matched_unique = sorted(list(set(matched)))
        missing_unique = sorted(list(set(missing)))
        
        logger.info("Processed candidate: '%s' | Edu: %s | Exp: %d yrs | Internships: %d | Skills: %d matched, %d missing",
                    candidate_name, candidate_education, candidate_experience, candidate_internships,
                    len(matched_unique), len(missing_unique))

        processed_resumes.append({
            "filename": filename,
            "name": candidate_name,
            "email": candidate_email,
            "phone": candidate_phone,
            "linkedin": candidate_linkedin,
            "github": candidate_github,
            "experience": candidate_experience,
            "internships": candidate_internships,
            "education": candidate_education,
            "projects": candidate_projects,
            "text": clean_text,
            "matched_skills": matched_unique,
            "missing_skills": missing_unique
        })
        
    # Rank candidates using scoring logic
    ranked_candidates = rank_candidates(jd_skills, processed_resumes)
    logger.info("Ranking complete — %d candidates scored", len(ranked_candidates))
    
    # Clean up output (remove large text payload)
    final_response = []
    for cand in ranked_candidates:
        cand_dict = {
            "filename": cand["filename"],
            "name": cand["name"],
            "email": cand["email"],
            "phone": cand["phone"],
            "linkedin": cand.get("linkedin", "Not Provided"),
            "github": cand.get("github", "Not Provided"),
            "experience": cand.get("experience", 0),
            "education": cand.get("education", "None"),
            "projects": cand.get("projects", 0),
            "similarity_score": cand["similarity_score"],
            "skill_score": cand.get("skill_score", 0),
            "experience_score": cand.get("experience_score", 0),
            "education_score": cand.get("education_score", 0),
            "projects_score": cand.get("projects_score", 0),
            "rank": cand["rank"],
            "matched_skills": cand["matched_skills"],
            "missing_skills": cand["missing_skills"]
        }
        final_response.append(cand_dict)
        
    elapsed = round(time.time() - start_time, 2)
    for cand in final_response:
        logger.info("  #%d %-20s → Final: %.1f%% (Skill: %.1f | Exp: %.1f | Edu: %.1f | Proj: %.1f)",
                    cand["rank"], cand["name"], cand["similarity_score"],
                    cand["skill_score"], cand["experience_score"],
                    cand["education_score"], cand["projects_score"])
    logger.info("Request completed in %.2fs", elapsed)
    logger.info("=" * 60)

    return {
        "results": final_response, 
        "jd_skills": sorted(jd_skills)
    }

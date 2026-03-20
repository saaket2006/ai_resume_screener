from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import spacy
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("resume_screener")

# Ensure spacy model is present early
try:
    spacy.load("en_core_web_sm")
except OSError:
    logging.warning("Downloading en_core_web_sm model for spaCy")
    from spacy.cli import download
    download("en_core_web_sm")

from backend.services.document_service import extract_text
from backend.services.nlp_service import preprocess_text
from backend.services.skill_extractor import extract_skills
from backend.services.scoring_service import rank_candidates
from backend.services.info_extractor import extract_name, extract_email, extract_phone, extract_linkedin, extract_github, extract_experience, extract_education, extract_projects

app = FastAPI(title="AI Resume Screener API")

# Setup CORS to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Resume Screener API running."}

@app.post("/api/process")
async def process_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    start_time = time.time()
    logger.info("=" * 60)
    logger.info("New screening request: %d resume(s) uploaded", len(resumes))

    if not job_description:
        raise HTTPException(status_code=400, detail="Job description is required")
        
    if not resumes:
        raise HTTPException(status_code=400, detail="At least one resume must be uploaded")
        
    # Process Job Description
    clean_jd = preprocess_text(job_description)
    jd_skills = extract_skills(job_description) # raw is often better for exact matching
    logger.info("JD skills extracted (%d): %s", len(jd_skills), ", ".join(jd_skills))
    
    processed_resumes = []
    
    for resume in resumes:
        contents = await resume.read()
        filename = resume.filename
        
        # Extract text based on file type
        try:
            raw_text = extract_text(contents, filename)
        except ValueError as e:
            logger.error("  Skipping '%s': %s", filename, e)
            processed_resumes.append({
                "filename": filename,
                "name": "Unreadable File",
                "email": "N/A",
                "phone": "N/A",
                "matched_skills": [],
                "missing_skills": sorted(jd_skills)
            })
            continue
        
        # Extract candidate details directly from raw text before preprocessing
        candidate_name = extract_name(raw_text)
        candidate_email = extract_email(raw_text)
        candidate_phone = extract_phone(raw_text)
        candidate_linkedin = extract_linkedin(raw_text)
        candidate_github = extract_github(raw_text)
        candidate_experience = extract_experience(raw_text)
        candidate_education = extract_education(raw_text)
        candidate_projects = extract_projects(raw_text)
        
        # Preprocess text
        clean_text = preprocess_text(raw_text)
        
        # Resolve broad conceptual requirements using Semantic Expansions
        from backend.services.skill_expander import get_related_skills, is_skill_in_text
        import re
        
        raw_text_lower = raw_text.lower()
        matched = []
        missing = []
        
        for skill in jd_skills:
            related_skills, is_broad = get_related_skills(skill)
            
            # Check if the JD skill itself is explicitly in the resume
            has_exact = is_skill_in_text(skill, raw_text_lower)
            
            if is_broad and related_skills:
                # It's a broad category (e.g., 'Frontend')
                found_related = []
                
                for rs in related_skills:
                    if is_skill_in_text(rs, raw_text_lower):
                        found_related.append(rs)
                        
                # Real-world inference: If they have the exact broad term OR at least 1 related technology
                # e.g., if they know React, they natively know Frontend.
                if has_exact or len(found_related) >= 1:
                    matched.append(skill) # Give credit for the broad domain itself
                    matched.extend(found_related) # Include the specific tools found
                else:
                    # They missed the domain entirely and didn't mention any related tech
                    missing.append(skill)
                    
            else:
                # Regular strict precision match
                if has_exact:
                    matched.append(skill)
                else:
                    missing.append(skill)
                    
        # Remove duplicates
        matched_unique = sorted(list(set(matched)))
        missing_unique = sorted(list(set(missing)))
        logger.info("  '%s' | %s | %d yrs exp | Skills: %d matched, %d missing",
                    candidate_name, candidate_education, candidate_experience,
                    len(matched_unique), len(missing_unique))

        processed_resumes.append({
            "filename": filename,
            "name": candidate_name,
            "email": candidate_email,
            "phone": candidate_phone,
            "linkedin": candidate_linkedin,
            "github": candidate_github,
            "experience": candidate_experience,
            "education": candidate_education,
            "projects": candidate_projects,
            "text": clean_text,
            "matched_skills": matched_unique,
            "missing_skills": missing_unique
        })
        
    # Rank candidates using Percentage Fulfillment Math
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

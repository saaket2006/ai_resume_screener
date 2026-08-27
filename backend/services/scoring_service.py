from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import logging
import functools

logger = logging.getLogger("resume_screener")

@functools.lru_cache(maxsize=128)
def _get_tfidf_model(jd_skills_tuple):
    """
    Caches the TF-IDF vectorizer and JD matrix for a given set of JD skills.
    jd_skills_tuple is expected to be a tuple of strings.
    """
    jd_skills_text = " ".join(jd_skills_tuple)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_jd = vectorizer.fit_transform([jd_skills_text])
    return vectorizer, tfidf_jd

def rank_candidates(jd_skills: List[str], resumes: List[Dict]) -> List[Dict]:
    """
    Ranks resumes against a job description using TF-IDF and Cosine Similarity.
    To prevent generic English filler (like 'team' or 'motivated') from artificially inflating candidate scores, the TF-IDF vectorizer only evaluates the extracted technical skills list rather than the full unstructred document text.
    """
    if not jd_skills or not resumes:
        return []
    
    try:
        vectorizer, tfidf_jd = _get_tfidf_model(tuple(jd_skills))
        if len(vectorizer.vocabulary_) == 0:
            return resumes
            
        # For the resumes, ONLY serialize the technical skills that the system explicitly validated they possessed against the JD.
        resume_texts = [" ".join(r.get("matched_skills", [])) for r in resumes]
        tfidf_resumes = vectorizer.transform(resume_texts)
        
    except Exception as e:
        logger.error("TF-IDF vectorization failed: %s", e)
        return resumes
        
    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(tfidf_jd, tfidf_resumes).flatten()
    
    ranked_results = []
    for idx, resume in enumerate(resumes):
        # 1. Base Skill Score (0 to 100)
        # Use semantic_score if available (new analyses), fallback to TF-IDF score (historical compatibility)
        if "semantic_score" in resume:
            skill_score = float(resume["semantic_score"])
        else:
            skill_score = float(cosine_similarities[idx]) * 100
        
        # 2. Experience Score (Max 10 years for 100%)
        # Add 0.5 years equivalent for each relevant internship (matching JD skills)
        exp_years = resume.get("experience", 0)
        internships = resume.get("internships", 0)
        
        effective_exp_years = exp_years + (internships * 0.5)
        
        exp_score = min((effective_exp_years / 10.0) * 100, 100)
        
        # 3. Education Score
        education = resume.get("education", "None")
        if education == "PhD":
            edu_score = 100
        elif education == "Master":
            edu_score = 80
        elif education == "Bachelor":
            edu_score = 60
        else:
            edu_score = 20
            
        # 4. Projects Score (extract_projects returns 0-5)
        proj_score = (resume.get("projects", 0) / 5.0) * 100
        
        # Apply Weights dynamically from resolved scoring profile weights (Part 5)
        meta = resume.get("analysis_metadata", {})
        weights = meta.get("component_weights", {"skills": 0.50, "experience": 0.25, "education": 0.15, "projects": 0.10})
        
        skills_w = weights.get("skills", 0.50)
        experience_w = weights.get("experience", 0.25)
        education_w = weights.get("education", 0.15)
        projects_w = weights.get("projects", 0.10)
        
        final_score = (skill_score * skills_w) + (exp_score * experience_w) + (edu_score * education_w) + (proj_score * projects_w)
        logger.debug("  Scoring '%s': Skill=%.1f Exp=%.1f Edu=%.1f Proj=%.1f → Final=%.1f",
                     resume.get("name", "Unknown"), skill_score, exp_score, edu_score, proj_score, final_score)
        
        result = resume.copy()
        result["similarity_score"] = round(final_score, 2)
        result["skill_score"] = round(skill_score, 2)
        result["experience_score"] = round(exp_score, 2)
        result["education_score"] = round(edu_score, 2)
        result["projects_score"] = round(proj_score, 2)
        
        ranked_results.append(result)
        
    # Sort by score descending (TF-IDF Cosine natively resolves ties using matrix weights)
    ranked_results.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    # Assign rank
    for rank, result in enumerate(ranked_results, 1):
        result["rank"] = rank
        
    return ranked_results

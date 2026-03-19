from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

def rank_candidates(jd_skills: List[str], resumes: List[Dict]) -> List[Dict]:
    """
    Ranks resumes against a job description using TF-IDF and Cosine Similarity.
    To prevent generic English filler (like 'team' or 'motivated') from artificially inflating candidate scores, the TF-IDF vectorizer only evaluates the extracted technical skills list rather than the full unstructred document text.
    """
    if not jd_skills or not resumes:
        return []

    # Join the pure JD skills into a single space-separated string block
    jd_skills_text = " ".join(jd_skills)
    
    # Fit the Vectorizer exactly to the Job Description's required skills
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_jd = vectorizer.fit_transform([jd_skills_text])
        if len(vectorizer.vocabulary_) == 0:
            return resumes
            
        # For the resumes, ONLY serialize the technical skills that the system explicitly validated they possessed against the JD.
        resume_texts = [" ".join(r.get("matched_skills", [])) for r in resumes]
        tfidf_resumes = vectorizer.transform(resume_texts)
        
    except Exception as e:
        print(f"Error in vectorization: {e}")
        return resumes
        
    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(tfidf_jd, tfidf_resumes).flatten()
    
    ranked_results = []
    for idx, resume in enumerate(resumes):
        # 1. Base TF-IDF Skill Score (0 to 100)
        skill_score = float(cosine_similarities[idx]) * 100
        
        # 2. Experience Score (Max 10 years for 100%)
        exp_years = resume.get("experience", 0)
        exp_score = min((exp_years / 10.0) * 100, 100)
        
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
        
        # Apply Weights
        # Skills: 50%, Experience: 25%, Education: 15%, Projects: 10%
        final_score = (skill_score * 0.50) + (exp_score * 0.25) + (edu_score * 0.15) + (proj_score * 0.10)
        
        result = resume.copy()
        result["similarity_score"] = round(final_score, 2)
        result["skill_score"] = round(skill_score, 2)
        
        ranked_results.append(result)
        
    # Sort by score descending (TF-IDF Cosine natively resolves ties using matrix weights)
    ranked_results.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    # Assign rank
    for rank, result in enumerate(ranked_results, 1):
        result["rank"] = rank
        
    return ranked_results

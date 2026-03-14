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
        score = float(cosine_similarities[idx])
        result = resume.copy()
        result["similarity_score"] = round(score * 100, 2)
        ranked_results.append(result)
        
    # Sort by score descending (TF-IDF Cosine natively resolves ties using matrix weights)
    ranked_results.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    # Assign rank
    for rank, result in enumerate(ranked_results, 1):
        result["rank"] = rank
        
    return ranked_results

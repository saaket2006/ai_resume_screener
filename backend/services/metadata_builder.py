import datetime
from typing import Dict, Any, List

def build_analysis_metadata(
    candidate_result: Dict[str, Any],
    processing_time_ms: int,
    parser: str,
    document_type: str,
    semantic_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Builds a standardized analysis_metadata dictionary according to the Phase 5 schema.
    This prepares the ATS engine for future Semantic, XAI, Confidence, and LLM capability updates
    while keeping the data structure robust and extensible.
    """
    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    
    semantic_dict = {
        "enabled": True,
        "exact_matches": semantic_data.get("exact_matches", []),
        "alias_matches": semantic_data.get("alias_matches", []),
        "hierarchical_matches": semantic_data.get("hierarchical_matches", []),
        "family_matches": semantic_data.get("family_matches", []),
        "semantic_score": semantic_data.get("semantic_score", 0.0)
    } if semantic_data else {
        "enabled": False,
        "exact_matches": [],
        "alias_matches": [],
        "hierarchical_matches": [],
        "family_matches": [],
        "semantic_score": 0.0
    }
    
    return {
        "engine": {
            "version": "1.0",
            "timestamp": now_iso,
            "processing_time_ms": processing_time_ms,
            "parser": parser,
            "document_type": document_type
        },
        "skills": {
            "extracted": candidate_result.get("matched_skills", []),  # All candidate skills
            "matched": candidate_result.get("matched_skills", []),
            "missing": candidate_result.get("missing_skills", [])
        },
        "semantic": semantic_dict,
        "score": {
            "overall": candidate_result.get("similarity_score", 0.0),
            "categories": {
                "skill_score": candidate_result.get("skill_score", 0.0),
                "experience_score": candidate_result.get("experience_score", 0.0),
                "education_score": candidate_result.get("education_score", 0.0),
                "projects_score": candidate_result.get("projects_score", 0.0),
                "semantic_score": semantic_dict["semantic_score"]
            }
        },
        "xai": {
            "enabled": False,
            "explanations": {}
        },
        "confidence": {
            "enabled": False,
            "level": None,
            "details": {}
        },
        "llm": {
            "enabled": False,
            "provider": None,
            "model": None,
            "generated": False
        },
        # Candidate Info holds contact info and summaries to preserve historical snapshot viewing
        "candidate": {
            "name": candidate_result.get("name", "N/A"),
            "email": candidate_result.get("email", "N/A"),
            "phone": candidate_result.get("phone", "N/A"),
            "linkedin": candidate_result.get("linkedin", "Not Provided"),
            "github": candidate_result.get("github", "Not Provided"),
            "experience": candidate_result.get("experience", 0),
            "education": candidate_result.get("education", "None"),
            "projects": candidate_result.get("projects", 0)
        }
    }

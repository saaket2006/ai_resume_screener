from typing import List, Any
from backend.services.recommendations.models import Recommendation
from backend.services.recommendations.heuristics import generate_heuristics_recommendations
from backend.services.recommendations.prioritizer import prioritize_recommendations
from backend.services.recommendations.llm_enhancer import enhance_recommendations_with_llm

def build_resume_recommendations(scoring_event: Any) -> List[Recommendation]:
    """
    Assembles, enhances, and prioritizes resume improvement recommendations from a ScoredEvent.
    """
    # 1. Generate base deterministic recommendations from local heuristics
    recs = generate_heuristics_recommendations(scoring_event)
    
    # 2. Optionally enhance wording with LLM if configured
    recs = enhance_recommendations_with_llm(recs)
    
    # 3. Prioritize by tier and gain
    recs = prioritize_recommendations(recs)
    
    return recs

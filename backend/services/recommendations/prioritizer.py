from typing import List
from backend.services.recommendations.models import Recommendation

def prioritize_recommendations(recommendations: List[Recommendation]) -> List[Recommendation]:
    """
    Sorts recommendations:
    1. Priority level (CRITICAL > HIGH > MEDIUM > LOW)
    2. Estimated score gain (descending)
    """
    priority_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }
    
    # Sort by priority index first, then by estimated_score_gain descending
    sorted_recs = sorted(
        recommendations,
        key=lambda r: (priority_order.get(r.priority.upper(), 4), -r.estimated_score_gain)
    )
    return sorted_recs

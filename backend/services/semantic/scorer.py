from typing import List, Dict, Any
from backend.services.semantic.models import MatchResult

class SemanticScorer:
    """
    Scoring Engine. Computes semantic match scores from lists of MatchResult.
    Responsible solely for score calculation, ensuring separation from match resolution.
    """
    def calculate_score(self, match_results: List[MatchResult]) -> Dict[str, Any]:
        if not match_results:
            return {
                "overall": 0.0,
                "breakdown": []
            }
            
        total_weight = 0.0
        breakdown = []
        
        for res in match_results:
            total_weight += res.weight
            breakdown.append({
                "required_skill": res.required_skill.canonical_name,
                "candidate_skill": res.candidate_skill.canonical_name,
                "match_type": res.match_type,
                "confidence": res.confidence,
                "weight": res.weight,
                "reason": res.reason
            })
            
        overall_score = round((total_weight / len(match_results)) * 100, 2)
        
        return {
            "overall": overall_score,
            "breakdown": breakdown
        }

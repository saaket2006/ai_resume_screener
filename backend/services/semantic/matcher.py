from typing import List
from backend.services.skills.models import Skill
from backend.services.semantic.models import MatchResult
from backend.services.semantic.resolver import resolve_relationship

class SemanticMatcher:
    """
    Core Semantic Matching Engine. Identifies relationships and maps required skills
    from the job description to the best-matching extracted candidate skills.
    """
    def match_skills(self, required_skills: List[Skill], candidate_skills: List[Skill]) -> List[MatchResult]:
        match_results = []
        
        for req in required_skills:
            best_result = None
            best_weight = -1.0
            
            for cand in candidate_skills:
                m_type, conf, weight, reason = resolve_relationship(req, cand)
                
                # We want to match the highest scoring relationship for this required skill
                if weight > best_weight:
                    best_weight = weight
                    best_result = MatchResult(
                        required_skill=req,
                        candidate_skill=cand,
                        match_type=m_type,
                        confidence=conf,
                        weight=weight,
                        reason=reason
                    )
            
            # If candidate had no matching skills, create a default UNKNOWN match result
            if best_result is None or best_weight <= 0.0:
                # Create dummy Skill representing candidate's lack of this skill
                empty_cand = Skill(
                    id="unknown",
                    canonical_name="None",
                    aliases=[],
                    abbreviations=[],
                    category="Unknown",
                    subcategory="Unknown",
                    technology_family="Unknown"
                )
                best_result = MatchResult(
                    required_skill=req,
                    candidate_skill=empty_cand,
                    match_type="UNKNOWN",
                    confidence=0.0,
                    weight=0.0,
                    reason=f"No match found for required skill {req.canonical_name}"
                )
                
            match_results.append(best_result)
            
        return match_results

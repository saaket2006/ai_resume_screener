from pydantic import BaseModel
from typing import List, Dict, Any
from backend.services.skills.models import Skill

class MatchResult(BaseModel):
    """
    Universal domain object representing a semantic match between a required skill
    from a job description and an extracted candidate skill.
    """
    required_skill: Skill
    candidate_skill: Skill
    match_type: str  # EXACT | ALIAS | ABBREVIATION | HIERARCHICAL | TECHNOLOGY_FAMILY | UNKNOWN
    confidence: float
    weight: float
    reason: str

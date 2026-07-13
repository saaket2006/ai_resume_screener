from pydantic import BaseModel
from typing import List, Optional

class Skill(BaseModel):
    id: str
    canonical_name: str
    aliases: List[str] = []
    abbreviations: List[str] = []
    category: str
    subcategory: str
    technology_family: str

class NormalizedSkill(BaseModel):
    skill: Skill
    match_type: str  # exact | alias | abbreviation | unknown
    confidence: float

from pydantic import BaseModel, Field
from typing import List, Optional

class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # Skills, Experience, Education, Projects, General
    reason: str
    source: str    # RULE, SEMANTIC, XAI, LLM
    related_skills: List[str] = Field(default_factory=list)
    estimated_score_gain: float
    confidence: float
    status: str = "active"

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Evidence(BaseModel):
    type: str  # e.g., "exact_match", "alias_match", "abbreviation_match", "hierarchical_match", "family_match", "unmatched", "experience_record", "education_level", "project_count", "document_similarity"
    category: str
    title: str
    description: str
    importance: str  # "high", "medium", "low"
    related_skill: Optional[str] = None
    confidence: float

class ScoreComponent(BaseModel):
    name: str
    raw_score: float
    weight: float
    weighted_score: float
    max_score: float
    status: str  # "met", "partially_met", "not_met", "exceeded"
    details: str
    evidence: List[Evidence]

class ExplanationItem(BaseModel):
    why_awarded: str
    why_deducted: str
    supporting_evidence: List[Evidence]

class StructuredExplanations(BaseModel):
    summary: ExplanationItem
    detailed: ExplanationItem
    technical: ExplanationItem

from typing import List, Dict, Any, Optional
from backend.services.policy.scoring_policy import default_scoring_policy

def estimate_missing_skill_gain(weight: float, weights: Optional[Dict[str, float]] = None) -> float:
    """
    Calculates estimated overall ATS score improvement for acquiring a missing skill.
    Formula: skill_weight * skills_component_overall_weight * 100.
    """
    skills_w = weights.get("skills", default_scoring_policy.skills_weight) if weights else default_scoring_policy.skills_weight
    gain = weight * skills_w * 100.0
    return round(gain, 1)

def estimate_experience_gain(current_years: float, weights: Optional[Dict[str, float]] = None) -> float:
    """
    Calculates gain for increasing experience details up to maximum scoring threshold.
    """
    max_yrs = default_scoring_policy.max_experience_years
    if current_years >= max_yrs:
        return 0.0
    # Gain for showing 1 extra year of experience
    exp_w = weights.get("experience", default_scoring_policy.experience_weight) if weights else default_scoring_policy.experience_weight
    gain = (1.0 / max_yrs) * exp_w * 100.0
    return round(gain, 1)

def estimate_education_gain(current_education: str, weights: Optional[Dict[str, float]] = None) -> float:
    """
    Calculates potential score gain from certifications or advanced coursework.
    """
    # Bachelor score is 60, Master score is 80, PhD is 100.
    # Certifications can improve non-PhD scores.
    if current_education == "PhD":
        return 0.0
    
    edu_w = weights.get("education", default_scoring_policy.education_weight) if weights else default_scoring_policy.education_weight
    if current_education == "Master":
        return round(20.0 * edu_w, 1)  # Gain to PhD equivalent
    elif current_education == "Bachelor":
        return round(20.0 * edu_w, 1)  # Gain to Master equivalent
    else:
        return round(40.0 * edu_w, 1)  # Gain to Bachelor equivalent

def estimate_project_gain(current_count: int, weights: Optional[Dict[str, float]] = None) -> float:
    """
    Calculates gain for adding one additional matching technical project.
    """
    target = default_scoring_policy.project_target_count
    if current_count >= target:
        return 0.0
    proj_w = weights.get("projects", default_scoring_policy.projects_weight) if weights else default_scoring_policy.projects_weight
    gain = (1.0 / target) * proj_w * 100.0
    return round(gain, 1)

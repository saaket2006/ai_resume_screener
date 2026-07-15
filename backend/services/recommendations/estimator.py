from typing import List, Dict, Any
from backend.services.policy.scoring_policy import default_scoring_policy

def estimate_missing_skill_gain(weight: float) -> float:
    """
    Calculates estimated overall ATS score improvement for acquiring a missing skill.
    Formula: skill_weight * skills_component_overall_weight * 100.
    Since skills weigh 50% of the total score, a skill with weight w contributes w * 50 points.
    """
    gain = weight * default_scoring_policy.skills_weight * 100.0
    return round(gain, 1)

def estimate_experience_gain(current_years: float) -> float:
    """
    Calculates gain for increasing experience details up to maximum scoring threshold.
    """
    max_yrs = default_scoring_policy.max_experience_years
    if current_years >= max_yrs:
        return 0.0
    # Gain for showing 1 extra year of experience
    gain = (1.0 / max_yrs) * default_scoring_policy.experience_weight * 100.0
    return round(gain, 1)

def estimate_education_gain(current_education: str) -> float:
    """
    Calculates potential score gain from certifications or advanced coursework.
    """
    # Bachelor score is 60, Master score is 80, PhD is 100.
    # Certifications can improve non-PhD scores.
    if current_education == "PhD":
        return 0.0
    elif current_education == "Master":
        return round(20.0 * default_scoring_policy.education_weight, 1)  # Gain to PhD equivalent
    elif current_education == "Bachelor":
        return round(20.0 * default_scoring_policy.education_weight, 1)  # Gain to Master equivalent
    else:
        return round(40.0 * default_scoring_policy.education_weight, 1)  # Gain to Bachelor equivalent

def estimate_project_gain(current_count: int) -> float:
    """
    Calculates gain for adding one additional matching technical project.
    """
    target = default_scoring_policy.project_target_count
    if current_count >= target:
        return 0.0
    gain = (1.0 / target) * default_scoring_policy.projects_weight * 100.0
    return round(gain, 1)

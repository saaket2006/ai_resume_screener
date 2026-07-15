class RecommendationPolicy:
    """
    Defines thresholds and priorities for AI Resume Improvement Engine recommendations.
    """
    def __init__(
        self,
        critical_threshold: float = 40.0,            # Component raw score below 40% makes a gap CRITICAL
        high_threshold: float = 70.0,                # Component raw score below 70% makes a gap HIGH
        critical_missing_skill_weight: float = 0.8,   # If missing skill weight >= 0.8, it is CRITICAL
        high_missing_skill_weight: float = 0.4,       # If missing skill weight >= 0.4, it is HIGH
        min_confidence: float = 0.5,                  # Minimum confidence cutoff for recommendations
        max_skills_recommendations: int = 5           # Limit on missing skills recommended
    ):
        self.critical_threshold = critical_threshold
        self.high_threshold = high_threshold
        self.critical_missing_skill_weight = critical_missing_skill_weight
        self.high_missing_skill_weight = high_missing_skill_weight
        self.min_confidence = min_confidence
        self.max_skills_recommendations = max_skills_recommendations

# Default global recommendation policy instance
default_recommendation_policy = RecommendationPolicy()

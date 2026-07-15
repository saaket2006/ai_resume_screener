class ScoringProfilePolicy:
    """
    Defines policy configurations and fallback weights for adaptive scoring profiles.
    Helps avoid magic numbers when handling weights validation and defaults.
    """
    def __init__(
        self,
        default_weights: dict = None,
        min_weight_sum: float = 0.99,
        max_weight_sum: float = 1.01
    ):
        self.default_weights = default_weights or {
            "skills": 0.50,
            "experience": 0.25,
            "education": 0.15,
            "projects": 0.10
        }
        self.min_weight_sum = min_weight_sum
        self.max_weight_sum = max_weight_sum

# Default global scoring profile policy instance
default_scoring_profile_policy = ScoringProfilePolicy()

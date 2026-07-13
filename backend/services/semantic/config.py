import os
from typing import Dict

# Configurable semantic matching weights to allow tuning without code edits
SEMANTIC_WEIGHTS: Dict[str, float] = {
    "EXACT": float(os.getenv("SEMANTIC_WEIGHT_EXACT", "1.00")),
    "ALIAS": float(os.getenv("SEMANTIC_WEIGHT_ALIAS", "0.95")),
    "ABBREVIATION": float(os.getenv("SEMANTIC_WEIGHT_ABBREVIATION", "0.90")),
    "HIERARCHICAL": float(os.getenv("SEMANTIC_WEIGHT_HIERARCHICAL", "0.75")),
    "TECHNOLOGY_FAMILY": float(os.getenv("SEMANTIC_WEIGHT_TECHNOLOGY_FAMILY", "0.60")),
    "UNKNOWN": float(os.getenv("SEMANTIC_WEIGHT_UNKNOWN", "0.00")),
}

def get_weight(match_type: str) -> float:
    """Returns the matching weight for the given match type."""
    return SEMANTIC_WEIGHTS.get(match_type.upper(), 0.00)

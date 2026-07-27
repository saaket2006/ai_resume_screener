from typing import Dict, List
from backend.services.skills.loader import get_skills_loader

def get_taxonomy() -> Dict[str, Dict[str, List[str]]]:
    """
    Constructs and returns the technology hierarchy structure.
    Exposes the classification of skills under categories and subcategories:
    e.g. {
        "Programming Languages": {
            "General Purpose": ["Python"]
        }
    }
    """
    skills = get_skills_loader()
    taxonomy = {}
    for s in skills:
        cat = s.category or "Unknown"
        sub = s.subcategory or "General"
        if cat not in taxonomy:
            taxonomy[cat] = {}
        if sub not in taxonomy[cat]:
            taxonomy[cat][sub] = []
        taxonomy[cat][sub].append(s.canonical_name)
    return taxonomy

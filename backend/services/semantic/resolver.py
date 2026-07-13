from backend.services.skills.models import Skill
from backend.services.semantic.config import get_weight

def resolve_relationship(req: Skill, cand: Skill) -> tuple:
    """
    Evaluates relationship type, confidence, and matches between two Skill objects.
    Returns: (match_type, confidence, weight, reason)
    """
    req_name_lower = req.canonical_name.lower()
    cand_name_lower = cand.canonical_name.lower()
    req_id = req.id.lower()
    cand_id = cand.id.lower()

    # 1. EXACT Match
    if req_id == cand_id or req_name_lower == cand_name_lower:
        match_type = "EXACT"
        confidence = 1.0
        reason = "Exact keyword match"
        return match_type, confidence, get_weight(match_type), reason

    # 2. ALIAS Match
    req_aliases_lower = [a.lower() for a in req.aliases]
    cand_aliases_lower = [a.lower() for a in cand.aliases]
    if cand_name_lower in req_aliases_lower or req_name_lower in cand_aliases_lower:
        match_type = "ALIAS"
        confidence = 0.95
        reason = f"Matched via alias: {cand.canonical_name} is a known alias of {req.canonical_name}"
        return match_type, confidence, get_weight(match_type), reason

    # 3. ABBREVIATION Match
    req_abbrs_lower = [a.lower() for a in req.abbreviations]
    cand_abbrs_lower = [a.lower() for a in cand.abbreviations]
    if cand_name_lower in req_abbrs_lower or req_name_lower in cand_abbrs_lower:
        match_type = "ABBREVIATION"
        confidence = 0.90
        reason = f"Matched via abbreviation: {cand.canonical_name} is an abbreviation of {req.canonical_name}"
        return match_type, confidence, get_weight(match_type), reason

    # 4. HIERARCHICAL Match (Sibling framework/library under same category & subcategory)
    if (req.category == cand.category and 
        req.subcategory == cand.subcategory and 
        req.category != "Unknown" and 
        req.subcategory != "Unknown"):
        match_type = "HIERARCHICAL"
        confidence = 0.75
        reason = f"Matched via hierarchy: Both are {req.subcategory} under category {req.category}"
        return match_type, confidence, get_weight(match_type), reason

    # 5. TECHNOLOGY_FAMILY Match
    # 5.1 Same technology family (e.g. Flask & React don't share category, but check backend vs devops etc)
    if req.technology_family == cand.technology_family and req.technology_family != "Unknown":
        match_type = "TECHNOLOGY_FAMILY"
        confidence = 0.60
        reason = f"Matched via technology family: Both belong to {req.technology_family}"
        return match_type, confidence, get_weight(match_type), reason

    # 5.2 Direct family association (e.g. JD asks for "Backend Development" family and candidate has "FastAPI")
    if ((req_name_lower == cand.technology_family.lower() or 
         cand_name_lower == req.technology_family.lower()) and 
        req.technology_family != "Unknown"):
        match_type = "TECHNOLOGY_FAMILY"
        confidence = 0.60
        reason = f"Matched via technology family association: {cand.canonical_name} belongs to family {req.canonical_name}"
        return match_type, confidence, get_weight(match_type), reason

    # 6. UNKNOWN Match
    match_type = "UNKNOWN"
    confidence = 0.0
    reason = "No semantic relationship identified"
    return match_type, confidence, get_weight(match_type), reason

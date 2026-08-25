import json
import os
import spacy
from typing import List
import re
import logging

logger = logging.getLogger("resume_screener")

from backend.services.nlp_service import nlp

# A comprehensive list of real-world technical skills to ensure accuracy
# Extracted into a JSON file for better maintainability

def load_tech_skills() -> set:
    """Loads the raw tech skills from a JSON file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    kb_path = os.path.join(base_dir, "knowledge_base", "tech_skills.json")
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception as e:
        logger.error("Failed to load tech_skills.json: %s", e)
        return set()

TECH_SKILLS = load_tech_skills()


def extract_raw_skill_strings(text: str) -> List[str]:
    """
    Extracts key skills and technical terms as raw strings using a robust hybrid approach.
    """
    doc = nlp(text)
    skills = set()
    text_lower = text.lower()
    
    # 1. Exact match from predefined comprehensive dictionary
    for skill in TECH_SKILLS:
        if skill in text_lower:
            # Avoid partial matches inside other words (like "c" inside "react")
            pattern = r'(?<![a-zA-Z0-9\-])' + re.escape(skill) + r'(?![a-zA-Z0-9\-])'
            if re.search(pattern, text_lower):
                skills.add(skill)
    
    logger.debug("Dictionary skills found: %d", len(skills))
                
    # 2. Extract Acronyms dynamically using Regex (e.g., API, HTTP)
    # Filter out common non-skill acronyms and overly long acronyms
    NON_SKILL_ACRONYMS = {"CEO", "CTO", "CFO", "COO", "GPA", "LLC", "INC", "USA", "UK", "PDF", "CV", "ROI", "KPI", "B2B", "B2C", "PMP", "MBA", "PHD", "MS", "BS", "BA", "MA", "HR", "PR", "HTTP", "HTTPS", "QA", "VP", "SME"}
    
    for token in doc:
        is_acronym = bool(re.match(r'^[A-Z]{2,}(/[A-Z]{2,})?$', token.text))
        if is_acronym and token.text not in NON_SKILL_ACRONYMS and len(token.text) <= 6:
            skills.add(token.text.lower())
    
    logger.debug("Total skills extracted after acronym check: %d", len(skills))
            
    return sorted(list(skills))

def extract_skills(text: str):
    """
    Extracts key skills and technical terms and returns them as structured Skill domain objects.
    """
    from backend.services.skills.extractor import SkillExtractor
    extractor = SkillExtractor()
    return extractor.extract(text)

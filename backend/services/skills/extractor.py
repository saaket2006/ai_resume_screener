from typing import List
# We import from the existing string-based skill_extractor
from backend.services.skill_extractor import extract_raw_skill_strings as extract_raw_names
from backend.services.skills.models import Skill
from backend.services.skills.normalizer import SkillNormalizer

class SkillExtractor:
    """
    Coordinates matching/extraction of skill names from raw text blocks and normalizes
    them into structured Skill domain objects.
    """
    def __init__(self):
        self.normalizer = SkillNormalizer()

    def extract(self, text: str) -> List[Skill]:
        # 1. Run existing extraction to retrieve matched skill strings
        raw_names = extract_raw_names(text)
        
        # 2. Normalize each extracted skill name into a structured Skill domain object
        skills = []
        for name in raw_names:
            ns = self.normalizer.normalize(name)
            skills.append(ns.skill)
            
        return skills

from abc import ABC, abstractmethod
from typing import List
import json
import os
from backend.services.skills.models import Skill

class SkillRepository(ABC):
    """
    Abstract base class interface for loading the skill intelligence knowledge base.
    This enables easily switching to a relational database or remote API in the future
    without altering the core matching or normalisation logic.
    """
    @abstractmethod
    def load(self) -> List[Skill]:
        pass

class JsonSkillRepository(SkillRepository):
    """
    Repository implementing SkillRepository that loads structured skills data from a JSON file.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Skill]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Skills knowledge base file not found at: {self.file_path}")
            
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        skills = []
        for item in data:
            skills.append(Skill(
                id=item["id"],
                canonical_name=item["canonical_name"],
                aliases=item.get("aliases", []),
                abbreviations=item.get("abbreviations", []),
                category=item["category"],
                subcategory=item.get("subcategory", ""),
                technology_family=item.get("technology_family", "")
            ))
        return skills

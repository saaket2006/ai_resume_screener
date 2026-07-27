import os
from typing import List
import logging
from backend.services.skills.models import Skill
from backend.services.skills.registry import JsonSkillRepository

logger = logging.getLogger("resume_screener")

_cached_skills: List[Skill] = None

def get_skills_loader() -> List[Skill]:
    """
    Caching singleton loader that reads and parses the skill knowledge base exactly once,
    avoiding repeated JSON file reloading during high-volume ATS runs.
    """
    global _cached_skills
    if _cached_skills is None:
        # Determine the root knowledge_base/skills.json directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        kb_path = os.path.join(base_dir, "knowledge_base", "skills.json")
        
        if not os.path.exists(kb_path):
            # Fallback path inside the module directory
            kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base", "skills.json")
            
        logger.info("Initializing skill intelligence layer from: %s", kb_path)
        try:
            repo = JsonSkillRepository(kb_path)
            _cached_skills = repo.load()
            logger.info("Skill intelligence layer successfully loaded with %d structured skills.", len(_cached_skills))
        except Exception as e:
            logger.error("Failed to load skill intelligence knowledge base: %s. Falling back to empty list.", e)
            _cached_skills = []
            
    return _cached_skills

def reset_skills_loader_cache():
    """Utility function to clear cached skills for testing."""
    global _cached_skills
    _cached_skills = None

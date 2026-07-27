from backend.services.skills.models import Skill, NormalizedSkill
from backend.services.skills.loader import get_skills_loader

class SkillNormalizer:
    """
    Normalizes arbitrary skill strings extracted from resumes or job descriptions
    using structured matching against the cached Skill Knowledge Base.
    Supports Exact, Alias, Abbreviation, and validation-safe Unknown match types.
    """
    def __init__(self):
        # This will fetch the singleton cached skills list
        self.skills = get_skills_loader()

    def normalize(self, skill_name: str) -> NormalizedSkill:
        if not skill_name:
            return self._build_unknown("")

        cleaned = skill_name.strip()
        cleaned_lower = cleaned.lower()

        # 1. Exact Match Check (canonical_name, stable id, or namespace-stripped id)
        for s in self.skills:
            id_parts = s.id.split(".")
            simple_id = id_parts[-1] if len(id_parts) > 1 else s.id
            if s.canonical_name.lower() == cleaned_lower or s.id == cleaned_lower or simple_id == cleaned_lower:
                return NormalizedSkill(skill=s, match_type="exact", confidence=1.0)

        # 2. Alias Match Check (synonyms e.g. ReactJS -> React)
        for s in self.skills:
            for alias in s.aliases:
                if alias.lower() == cleaned_lower:
                    return NormalizedSkill(skill=s, match_type="alias", confidence=0.9)

        # 3. Abbreviation Match Check (e.g. LLM -> Large Language Models)
        for s in self.skills:
            for abbr in s.abbreviations:
                if abbr.lower() == cleaned_lower:
                    return NormalizedSkill(skill=s, match_type="abbreviation", confidence=0.8)

        # 4. Unknown/Temporary Skill fallback (no matching entry in knowledge base)
        return self._build_unknown(cleaned)

    def _build_unknown(self, raw_name: str) -> NormalizedSkill:
        cleaned_id = raw_name.lower().replace(" ", "_") if raw_name else "unknown"
        temp_skill = Skill(
            id=cleaned_id,
            canonical_name=raw_name or "Unknown",
            aliases=[],
            abbreviations=[],
            category="Unknown",
            subcategory="Unknown",
            technology_family="Unknown"
        )
        return NormalizedSkill(skill=temp_skill, match_type="unknown", confidence=0.0)

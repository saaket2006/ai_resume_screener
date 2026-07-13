import re

def validate_skill_name(name: str) -> bool:
    """
    Validates that a skill name contains reasonable characters and isn't empty,
    allowing common tech formats like C++, C#, .NET, Node.js, and CI/CD.
    """
    if not name or not isinstance(name, str):
        return False
    trimmed = name.strip()
    if not trimmed or len(trimmed) > 100:
        return False
    # Validate character whitelist for technical names
    return bool(re.match(r'^[a-zA-Z0-9\s\+\-\#\.\/\&]+$', trimmed))

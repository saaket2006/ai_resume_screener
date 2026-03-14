# A dictionary mapping broad concepts to specific tools/languages.
# If the Job Description asks for the key, the system will also count the values as exact matches.
SEMANTIC_SKILL_EXPANSIONS = {
    "web development": ["html", "css", "javascript", "react", "vue", "angular", "node.js", "frontend", "backend", "web"],
    "frontend": ["html", "css", "javascript", "react", "vue", "angular", "ui", "ux", "web design", "bootstrap", "tailwind"],
    "backend": ["python", "java", "node.js", "ruby", "php", "go", "c#", "sql", "api", "rest", "graphql", "database", "server", "fastapi", "django", "spring"],
    "machine learning": ["python", "scikit-learn", "tensorflow", "pytorch", "keras", "pandas", "numpy", "models", "data science", "ai", "artificial intelligence"],
    "artificial intelligence": ["machine learning", "deep learning", "nlp", "computer vision", "generative ai", "llm", "neural networks", "ai"],
    "ai": ["machine learning", "deep learning", "nlp", "computer vision", "generative ai", "llm", "neural networks", "artificial intelligence"],
    "generative ai": ["llm", "chatgpt", "openai", "claude", "prompt engineering", "langchain", "agents", "multi-agent"],
    "nlp": ["natural language processing", "spacy", "nltk", "transformers", "huggingface", "text classification", "llm"],
    "data science": ["python", "r", "pandas", "numpy", "sql", "machine learning", "statistics", "data analysis", "tableau", "visualization"],
    "databases": ["sql", "mysql", "postgresql", "mongodb", "nosql", "redis", "oracle", "cassandra"],
    "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "cloud computing", "serverless"],
    "devops": ["ci/cd", "jenkins", "docker", "kubernetes", "terraform", "ansible", "git", "linux", "aws"],
    "object-oriented programming": ["oop", "java", "c++", "c#", "python"],
    "oop": ["object-oriented programming", "java", "c++", "c#", "python"],
    "software development": ["java", "python", "c++", "c#", "javascript", "git", "agile", "sql", "testing", "ci/cd", "oop", "architecture"],
    "software engineering": ["java", "python", "c++", "c#", "javascript", "git", "agile", "sql", "testing", "ci/cd", "oop", "architecture"]
}

def get_related_skills(skill: str) -> tuple[list[str], bool]:
    """
    Checks if an explicit skill contains a broad conceptual keyword.
    For example, "Full Stack Web Development" contains "web development".
    Returns (list_of_related_skills, is_broad_concept).
    """
    skill_lower = skill.lower()
    for broad_keyword, related in SEMANTIC_SKILL_EXPANSIONS.items():
        if broad_keyword in skill_lower:
            return related, True
            
    return [], False

SKILL_ALIASES = {
    "react": ["react.js", "reactjs"],
    "node.js": ["node", "nodejs"],
    "vue": ["vue.js", "vuejs"],
    "angular": ["angularjs"],
    "kubernetes": ["k8s"],
    "amazon web services": ["aws"],
    "google cloud platform": ["gcp"],
    "machine learning": ["ml", "machine-learning"],
    "deep learning": ["dl", "deep-learning"],
    "artificial intelligence": ["ai"],
    "generative ai": ["genai", "gen-ai"],
    "natural language processing": ["nlp"]
}

def is_skill_in_text(skill: str, text_lower: str) -> bool:
    """
    Checks if a skill or any of its known aliases exists in the given text.
    Handles exact Word Boundary matching for accuracy.
    """
    import re
    skill_lower = skill.lower()
    
    # Collect all possible valid strings for this skill
    valid_terms = {skill_lower}
    
    # If the skill is a known root, add its aliases
    if skill_lower in SKILL_ALIASES:
        valid_terms.update(SKILL_ALIASES[skill_lower])
        
    # If the skill IS an alias, add the root and all sibling aliases
    for key, aliases in SKILL_ALIASES.items():
        if skill_lower in aliases:
            valid_terms.add(key)
            valid_terms.update(aliases)
            
    # Check all collected variants against the text using Word Boundaries
    for term in valid_terms:
        pattern = r'(?<![a-zA-Z0-9\-])' + re.escape(term) + r'(?![a-zA-Z0-9\-])'
        if re.search(pattern, text_lower):
            return True
            
    return False

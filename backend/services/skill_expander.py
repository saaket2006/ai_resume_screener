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

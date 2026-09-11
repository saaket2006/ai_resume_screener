import re

def extract_email(text: str) -> str:
    """Extract the first email found in the text."""
    # Clean up common PDF rendering template icon garble (e.g. envelope icons rendering as 'envel⌢pe' merging into the email)
    clean_text = re.sub(r'envel[^\w]?pe', ' ', text, flags=re.IGNORECASE)
    
    # Common email regex pattern
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, clean_text)
    return match.group(0) if match else "Not Provided"

def extract_linkedin(text: str) -> str:
    """Extract a LinkedIn profile URL."""
    clean_text = re.sub(r'(?:/)?linkedin(linkedin\.com)', r'\1', text, flags=re.IGNORECASE)
    clean_text = re.sub(r'envel[^\w]?pe', ' ', clean_text, flags=re.IGNORECASE)
    pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in/|in)?(?:[A-Za-z0-9_-]+)/?'
    match = re.search(pattern, clean_text, flags=re.IGNORECASE)
    return match.group(0) if match else "Not Provided"

def extract_github(text: str) -> str:
    """Extract a GitHub profile URL."""
    clean_text = re.sub(r'(?:/)?github(github\.com)', r'\1', text, flags=re.IGNORECASE)
    clean_text = re.sub(r'envel[^\w]?pe', ' ', clean_text, flags=re.IGNORECASE)
    pattern = r'(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+/?'
    match = re.search(pattern, clean_text, flags=re.IGNORECASE)
    return match.group(0) if match else "Not Provided"

def extract_phone(text: str) -> str:
    """Extract a phone number found in the text."""
    # Pattern to match standard formats including country codes and extensions
    # e.g. +1 555-019-2834, +44 7700 900123, (123) 456-7890
    pattern = r'(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    
    # Check for UK style or spaced out formats
    pattern_alt = r'\+?\d{1,4}\s?\d{3,4}\s?\d{4,6}'
    match_alt = re.search(pattern_alt, text)
    return match_alt.group(0).strip() if match_alt else "Not Provided"

DISQUALIFIED_NAME_WORDS = {
    'engineer', 'developer', 'architect', 'scientist', 'analyst', 'manager',
    'lead', 'consultant', 'specialist', 'designer', 'administrator', 'director',
    'officer', 'intern', 'assistant', 'associate', 'programmer', 'coder',
    'summary', 'experience', 'education', 'skills', 'projects', 'profile',
    'objective', 'certifications', 'contact', 'curriculum', 'vitae', 'resume',
    'portfolio', 'references', 'employment', 'technical', 'competencies',
    'qualification', 'qualifications', 'background', 'activities', 'honors',
    'awards', 'languages', 'hobbies', 'interests', 'phone', 'email', 'linkedin',
    'github', 'address', 'city', 'state', 'zip', 'country', 'details', 'about'
}

def extract_name(text: str) -> str:
    """
    Attempt to extract a candidate's name.
    As a heuristic for unstructured resumes, we assume the name is in the first few non-empty lines,
    typical of header sections, while rejecting common job titles and section headers.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    for line in lines[:8]:
        # Strip common header junk like "Resume" or "CV"
        clean_line = re.sub(r'^(RESUME|CV|CURRICULUM VITAE)$', '', line, flags=re.IGNORECASE).strip()
        if not clean_line:
            continue

        # If it has 2 to 4 words and is mostly letters/dashes/periods
        words = clean_line.split()
        if 1 < len(words) < 5 and re.match(r'^[A-Za-z\s\-\.]+$', clean_line):
            # Check whether any word in the line is an obvious job title or section heading keyword
            lower_words = [w.lower().strip('.,-') for w in words]
            if any(w in DISQUALIFIED_NAME_WORDS for w in lower_words):
                continue
            return clean_line

    return "Not Provided"

def extract_experience(text: str) -> int:
    """
    Heuristically extract total years of experience.
    Looks for phrases like "5 years of experience", "10+ years", etc.
    """
    pattern = r'(\d+)(?:\+|[\+ \w]*)\s*(?:years?|yrs?|yr)\s*(?:of\s*)?experience'
    matches = re.finditer(pattern, text, flags=re.IGNORECASE)
    years = [int(match.group(1)) for match in matches]
    return max(years) if years else 0

INTERN_PATTERN = re.compile(r'\bintern(?:s|ship|ships)?\b')

_skills_regex_cache = {}

def extract_relevant_internships(text: str, jd_skills: list[str]) -> int:
    """
    Heuristically extract the number of internships that match the JD skills.
    We split text by lines/paragraphs and if an internship is mentioned near a JD skill, we count it.
    """
    if not jd_skills:
        return 0
        
    text_lower = text.lower()
    
    # Split text into rough chunks (paragraphs or large bullet blocks)
    chunks = re.split(r'\n\s*\n', text_lower)
    
    internship_count = 0

    unique_skills = frozenset(skill.lower() for skill in jd_skills)
    if unique_skills not in _skills_regex_cache:
        # Sort by length descending to match longer phrases first if they overlap
        sorted_skills = sorted(list(unique_skills), key=len, reverse=True)
        # Using exact substring match without word boundaries to preserve original behavior
        # where any(skill in chunk) was used.
        pattern = re.compile('|'.join(map(re.escape, sorted_skills)))
        _skills_regex_cache[unique_skills] = pattern

    skills_pattern = _skills_regex_cache[unique_skills]
    
    for chunk in chunks:
        if INTERN_PATTERN.search(chunk):
            # Check if any JD skill is in this chunk
            if skills_pattern.search(chunk):
                internship_count += 1
                
    return internship_count

def extract_education(text: str) -> str:
    """
    Heuristically extract highest degree level.
    Returns standard labels for weighting ("PhD", "Master", "Bachelor", "None").
    Carefully handles acronyms like M.E., B.E., M.S. to prevent false positives
    from ordinary English words like 'me', 'be', or tool names like 'MS Excel'.
    """
    if not text:
        return "None"

    text_lower = text.lower()

    # 1. PhD / Doctorate
    if re.search(r'\b(ph\.?d|doctorate|doctor\s+of\s+philosophy)\b', text_lower):
        return "PhD"

    # Mask out Microsoft products to prevent false MS degree detection
    cleaned_text = re.sub(
        r'\bms\s+(?:excel|office|word|powerpoint|teams|azure|sql|access|dos|project|dynamics|visio|paint)\b',
        ' ',
        text_lower
    )

    # 2. Master Degree
    # Unambiguous full words & clear acronyms
    if re.search(r'\b(masters?|mba|m\.?tech|master\s+of\s+[a-z]+)\b', cleaned_text):
        return "Master"
    # Dotted abbreviations: M.S., M.S, M.A., M.A, M.E., M.E (never matches plain "me" or "ms")
    if re.search(r'\b(m\.s\.|m\.s|m\.a\.|m\.a|m\.e\.|m\.e)\b', cleaned_text):
        return "Master"
    # Undotted MS / ME with explicit degree context (e.g. "MS in Computer Science", "ME Computer Science")
    if re.search(r'\b(ms|me)\s+(?:in|of)\s+[a-z]+', cleaned_text):
        return "Master"
    if re.search(r'\b(ms|me)\s+(?:computer|software|data|electrical|mechanical|civil|aerospace|biomedical|chemical|engineering|science|it|cs|ai|ml)\b', cleaned_text):
        return "Master"
    if re.search(r'(?:degree\s+(?:of|in)|completed\s+(?:my\s+)?|pursuing\s+(?:a\s+)?|holding\s+(?:a\s+)?|holds\s+(?:a\s+)?)\s*(?:an?\s+)?\b(ms|me)\b', cleaned_text):
        return "Master"

    # 3. Bachelor Degree
    # Unambiguous full words & clear acronyms
    if re.search(r'\b(bachelors?|b\.?tech|bachelor\s+of\s+[a-z]+|undergraduate)\b', cleaned_text):
        return "Bachelor"
    # Dotted abbreviations: B.S., B.S, B.A., B.A, B.E., B.E (never matches plain "be" or "bs")
    if re.search(r'\b(b\.s\.|b\.s|b\.a\.|b\.a|b\.e\.|b\.e)\b', cleaned_text):
        return "Bachelor"
    # Undotted BE / BS with explicit degree context (e.g. "BE in Mechanical", "BE Computer Science")
    if re.search(r'\b(be|bs)\s+(?:in|of)\s+[a-z]+', cleaned_text):
        return "Bachelor"
    if re.search(r'\b(be|bs)\s+(?:computer|software|data|electrical|mechanical|civil|aerospace|biomedical|chemical|engineering|science|it|cs)\b', cleaned_text):
        return "Bachelor"
    if re.search(r'(?:degree\s+(?:of|in)|completed\s+(?:my\s+)?|pursuing\s+(?:a\s+)?|holding\s+(?:a\s+)?|holds\s+(?:a\s+)?)\s*(?:an?\s+)?\b(be|bs)\b', cleaned_text):
        return "Bachelor"

    return "None"

def extract_projects(text: str) -> int:
    """
    Very crude heuristic to determine the scale or presence of personal/academic projects.
    Returns a score from 0 to 5 based on occurrences of 'project' or presence of a 'Projects' section.
    """
    text_lower = text.lower()
    # Check if there is a literal line that looks like a "Projects" header
    has_section = bool(re.search(r'^\s*(?:personal |academic )?projects?\s*$', text_lower, flags=re.MULTILINE))
    
    # Count the word project(s)
    project_count = len(re.findall(r'\bprojects?\b', text_lower))
    
    score = 0
    if has_section:
        score += 3
        
    # Give some points for generally talking about projects
    if project_count >= 5:
        score += 2
    elif project_count >= 2:
        score += 1
        
    return min(score, 5)  # Cap at 5 points

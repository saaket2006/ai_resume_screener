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

def extract_name(text: str) -> str:
    """
    Attempt to extract a candidate's name.
    As a heuristic for unstructured resumes, we assume the name is in the first few non-empty lines, typical of header sections.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # We'll take the first line that looks like a name (2-3 words capitalized or entirely capitalized)
    for line in lines[:5]:
        # Strip common header junk like "Resume" or "CV"
        clean_line = re.sub(r'^(RESUME|CV|CURRICULUM VITAE)$', '', line, flags=re.IGNORECASE).strip()
        
        # If it has 2 to 4 words and is mostly letters
        if 1 < len(clean_line.split()) < 5 and re.match(r'^[A-Za-z\s\-\.]+$', clean_line):
           # Extra split to avoid huge lines passing through
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

def extract_education(text: str) -> str:
    """
    Heuristically extract highest degree level.
    Returns standard labels for weighting.
    """
    text_lower = text.lower()
    
    # Check highest levels first
    if re.search(r'\b(ph\.?d|doctorate)\b', text_lower):
        return "PhD"
    if re.search(r'\b(master|m\.?s|m\.?a|mba|m\.?tech|m\.?e)\b', text_lower):
        return "Master"
    if re.search(r'\b(bachelor|b\.?s|b\.?a|b\.?tech|b\.?e|undergraduate)\b', text_lower):
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

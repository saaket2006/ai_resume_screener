import re

def extract_email(text: str) -> str:
    """Extract the first email found in the text."""
    # Common email regex pattern
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else "Unknown"

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
    return match_alt.group(0).strip() if match_alt else "Unknown"

def extract_name(text: str) -> str:
    """
    Attempt to extract a candidate's name.
    As a heuristic for unstructured resumes, we assume the name is 
    in the first few non-empty lines, typical of header sections.
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
           
    return "Candidate Name Not Found"

import pytest
from backend.services.info_extractor import extract_linkedin

def test_extract_linkedin_valid_urls():
    assert extract_linkedin("My profile is https://www.linkedin.com/in/johndoe") == "https://www.linkedin.com/in/johndoe"
    assert extract_linkedin("Contact me at http://linkedin.com/in/johndoe/") == "http://linkedin.com/in/johndoe/"
    assert extract_linkedin("www.linkedin.com/in/johndoe") == "www.linkedin.com/in/johndoe"
    assert extract_linkedin("linkedin.com/in/johndoe") == "linkedin.com/in/johndoe"
    assert extract_linkedin("linkedin.com/johndoe") == "linkedin.com/johndoe"
    assert extract_linkedin("https://linkedin.com/in/john-doe-1234") == "https://linkedin.com/in/john-doe-1234"
    assert extract_linkedin("https://linkedin.com/in/john_doe/") == "https://linkedin.com/in/john_doe/"
    # Extract only the relevant part, excluding following characters
    assert extract_linkedin("linkedin.com/in/johndoe is my URL") == "linkedin.com/in/johndoe"

def test_extract_linkedin_malformed_urls():
    # Test cleanup for repeating 'linkedin' text (common PDF parsing artifact)
    assert extract_linkedin("linkedinlinkedin.com/in/johndoe") == "linkedin.com/in/johndoe"
    assert extract_linkedin("/linkedinlinkedin.com/in/johndoe") == "linkedin.com/in/johndoe"

    # Test cleanup for envelope icon artifacts (e.g. envelope icons rendering as 'envel⌢pe' merging into the email)
    assert extract_linkedin("envel⌢pehttps://www.linkedin.com/in/johndoe") == "https://www.linkedin.com/in/johndoe"
    assert extract_linkedin("envelpe linkedin.com/in/johndoe") == "linkedin.com/in/johndoe"

def test_extract_linkedin_not_provided():
    assert extract_linkedin("I do not have a profile") == "Not Provided"
    assert extract_linkedin("github.com/johndoe") == "Not Provided"

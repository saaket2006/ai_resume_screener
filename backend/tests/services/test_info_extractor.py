import pytest
from backend.services.info_extractor import extract_linkedin, extract_education

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


def test_extract_education_phd():
    assert extract_education("I have a PhD in Computer Science.") == "PhD"
    assert extract_education("He is a Ph.D. graduate.") == "PhD"
    assert extract_education("She holds a Doctorate in Mathematics.") == "PhD"
    assert extract_education("Completed my doctorate in 2020.") == "PhD"

def test_extract_education_master():
    assert extract_education("I have a Master degree.") == "Master"
    assert extract_education("Completed my M.S. in CS.") == "Master"
    assert extract_education("Graduated with an M.A. in English.") == "Master"
    assert extract_education("I am pursuing an MBA.") == "Master"
    assert extract_education("Got my M.Tech from IIT.") == "Master"
    assert extract_education("Finished my M.E. program.") == "Master"
    assert extract_education("Received a master's in AI.") == "Master" # checks "master"

def test_extract_education_bachelor():
    assert extract_education("I have a Bachelor of Science.") == "Bachelor"
    assert extract_education("B.S. in Biology.") == "Bachelor"
    assert extract_education("She has a B.A. in Arts.") == "Bachelor"
    assert extract_education("B.Tech in Engineering.") == "Bachelor"
    assert extract_education("He holds a B.E.") == "Bachelor"
    assert extract_education("Undergraduate degree from state university.") == "Bachelor"
    assert extract_education("bachelor's degree") == "Bachelor"

def test_extract_education_none():
    assert extract_education("High school diploma.") == "None"
    assert extract_education("Some college coursework.") == "None"
    assert extract_education("I learned from online courses.") == "None"
    assert extract_education("") == "None"

def test_extract_education_precedence():
    # If multiple are present, the highest should be picked first
    assert extract_education("I have a Bachelor's degree and a Master's degree.") == "Master"
    assert extract_education("I got my B.S. before my Ph.D. and then an MBA.") == "PhD"
    assert extract_education("Started as undergraduate, then Master, now Doctorate") == "PhD"

def test_extract_education_case_insensitivity():
    assert extract_education("I HAVE A PHD") == "PhD"
    assert extract_education("master of science") == "Master"
    assert extract_education("BACHELOR DEGREE") == "Bachelor"

def test_extract_education_boundaries():
    # Ensuring it matches words properly and doesn't match substrings like "mastery" or "macerator"
    assert extract_education("I achieved mastery in python.") == "None"
    assert extract_education("The band name is Ph.D") == "PhD"

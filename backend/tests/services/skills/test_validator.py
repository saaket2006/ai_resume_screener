from backend.services.skills.validator import validate_skill_name


def test_validate_skill_name_valid_common():
    assert validate_skill_name("Python") is True
    assert validate_skill_name("JavaScript") is True
    assert validate_skill_name("React") is True
    assert validate_skill_name("SQL") is True


def test_validate_skill_name_valid_special_chars():
    assert validate_skill_name("C++") is True
    assert validate_skill_name("C#") is True
    assert validate_skill_name(".NET") is True
    assert validate_skill_name("Node.js") is True
    assert validate_skill_name("CI/CD") is True
    assert validate_skill_name("HTML/CSS") is True
    assert validate_skill_name("A & B") is True
    assert validate_skill_name("Problem-Solving") is True


def test_validate_skill_name_whitespace():
    assert validate_skill_name("   Python   ") is True
    assert validate_skill_name("Data Science") is True


def test_validate_skill_name_invalid_chars():
    assert validate_skill_name("Python@") is False
    assert validate_skill_name("Java!") is False
    assert validate_skill_name("React$") is False
    assert validate_skill_name("Ruby%20") is False
    assert validate_skill_name("Skills: Python") is False  # Invalid colon
    assert validate_skill_name("Python, Java") is False  # Invalid comma


def test_validate_skill_name_empty_or_whitespace_only():
    assert validate_skill_name("") is False
    assert validate_skill_name("   ") is False
    assert validate_skill_name("\n") is False


def test_validate_skill_name_non_string():
    assert validate_skill_name(None) is False
    assert validate_skill_name(123) is False
    assert validate_skill_name(["Python"]) is False
    assert validate_skill_name({"skill": "Python"}) is False


def test_validate_skill_name_too_long():
    long_skill = "a" * 101
    assert validate_skill_name(long_skill) is False

    # Boundary condition
    exact_limit_skill = "a" * 100
    assert validate_skill_name(exact_limit_skill) is True

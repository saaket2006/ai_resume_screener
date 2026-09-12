import pytest
from backend.services.document_service import extract_text

def test_extract_text_fallback_valid_utf8():
    """Test fallback extraction with valid UTF-8 text."""
    file_bytes = b"Hello, this is a plain text file."
    filename = "resume.txt"
    result = extract_text(file_bytes, filename)
    assert result == "Hello, this is a plain text file."

def test_extract_text_fallback_invalid_utf8():
    """Test fallback extraction with invalid UTF-8 bytes raises ValueError."""
    file_bytes = b"\xff\xfe" # Invalid UTF-8
    filename = "resume.unknown"
    with pytest.raises(ValueError, match="Unsupported file format or unreadable text encoding."):
        extract_text(file_bytes, filename)

def test_extract_text_doc_unsupported():
    """Test legacy .doc files raise ValueError."""
    file_bytes = b"dummy"
    filename = "resume.doc"
    with pytest.raises(ValueError, match="legacy binary format is not supported"):
        extract_text(file_bytes, filename)

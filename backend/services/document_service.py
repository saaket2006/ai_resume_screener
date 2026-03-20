import io
import PyPDF2
import docx
import logging

logger = logging.getLogger("resume_screener")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        logger.error("Failed to read PDF: %s", e)
        raise ValueError(f"Failed to read PDF file format: {e}")
    logger.debug("Successfully extracted %d characters from PDF", len(text))
    return text.strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        logger.error("Failed to read DOCX: %s", e)
        raise ValueError(f"Failed to read DOCX file format: {e}")
    logger.debug("Successfully extracted %d characters from DOCX", len(text))
    return text.strip()

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Route to appropriate extractor based on extension."""
    filename_lower = filename.lower()
    if filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith('.docx') or filename_lower.endswith('.doc'):
        return extract_text_from_docx(file_bytes)
    else:
        # Fallback for plain text or unsupported formats
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("Unsupported file format or unreadable text encoding.")

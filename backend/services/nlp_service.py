import spacy
import re
import string
import logging

# Ensure the model is loaded or downloaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logging.warning("Downloading en_core_web_sm model for spaCy")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> str:
    """
    Cleans text by:
    - Lowercasing
    - Removing punctuation
    - Removing stopwords
    - Lemmatization
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove URLS and email addresses (basic regex)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Use spaCy for lemmatization and stopword removal
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    
    return " ".join(tokens)

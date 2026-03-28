import re

"""
    preprocessing.py preprocesses text for SBERT embeddings.
    
    SBERT is trained on natural language and relies on full sentence structure 
    to build semantic representations. Removing stop words, lowercasing, 
    or custom tokenization degrades embedding quality.
    
    This module only removes technical artifacts that carry no semantic meaning
    (e.g. spurious whitespace, non-printable characters).
"""


def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    # Normalize multiple whitespace and spurious newlines
    text = re.sub(r'\s+', ' ', text)

    # Remove non-printable / corrupted unicode characters
    text = re.sub(r'[^\x20-\x7E]', ' ', text)

    return text.strip()

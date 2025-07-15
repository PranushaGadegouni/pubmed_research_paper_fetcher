import re
from .affiliation_classifier import classify_affiliation

def is_non_academic(affiliation: str) -> bool:
    return classify_affiliation(affiliation)

def extract_email(text: str) -> str:
    """Find the first email address in a block of text."""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else ""

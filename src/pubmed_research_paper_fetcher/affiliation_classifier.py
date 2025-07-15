import spacy

nlp = spacy.load("en_core_web_sm")

INDUSTRY_KEYWORDS = [
    "pharma", "biotech", "inc", "ltd", "corp", "gmbh", "solutions",
    "technologies", "company", "laboratories", "systems", "enterprises"
]

ACADEMIC_KEYWORDS = [
    "university", "institute", "college", "school", "faculty", "department",
    "hospital", "center", "centre", "academia", "research foundation", "clinic"
]

def classify_affiliation(affiliation: str) -> bool:
    affil_lower = affiliation.lower()

    # Explicit academic detection first
    if any(keyword in affil_lower for keyword in ACADEMIC_KEYWORDS):
        return False

    # Check for industry markers
    if any(keyword in affil_lower for keyword in INDUSTRY_KEYWORDS):
        return True

    # NER fallback
    doc = nlp(affiliation)
    for ent in doc.ents:
        if ent.label_ in ("ORG", "FAC"):
            if any(kw in ent.text.lower() for kw in INDUSTRY_KEYWORDS):
                return True

    return False

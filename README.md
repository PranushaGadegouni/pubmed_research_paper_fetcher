# PUBMED RESEARCH PAPER FETCHER

A Python-based command-line tool to fetch recent medical research papers from PubMed and extract details about **non-academic authors** and their **company affiliations**, using Named Entity Recognition (NER) with `spaCy`.

---

## Project Structure

pubmed_ner_fetcher/
│
├── src/
│ └── pubmed_research_paper_fetcher/
│ ├── cli.py # Command-line interface
│ ├── fetcher.py # Fetches data from PubMed API
│ ├── filters.py # Extracts filtered author and affiliation info
│ ├── utils.py # Utility to classify affiliations
│ ├── affiliation_classifier.py# NER-based affiliation classifier (spaCy)
│ └── init.py # Package initializer
│
├── pyproject.toml # Poetry dependency config
├── README.md # Project documentation

yaml
Copy
Edit

---

# Installation

Make sure you have [Python 3.10+](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/#installation) installed.

# Clone the repo
```bash
git clone <https://github.com/PranushaGadegouni/pubmed_research_paper_fetcher.git>
cd pubmed_research_paper_fetcher

# Install dependencies with Poetry
bash
Copy
Edit
poetry install

# Download spaCy's NER model
bash
Copy
Edit
poetry run python -m spacy download en_core_web_sm

# How to Use
Run the tool from the root project directory:
bash
Copy
Edit
poetry run get-papers-list --query "cancer vaccine" --file results.csv --debug

# Parameters
--query or -q: PubMed query (e.g., "cancer vaccine")
--file or -f: Output CSV file
--debug: (Optional) Enable debug logging

# Example Output
PMID	Title	Publication Date	Non-academic Author(s)	Company Affiliation(s)	Corresponding Author Email
40659123	Advances in Vaccine Platforms	2025-07-01	["Jane Doe"]	["Pfizer Inc."]	jane.doe@pfizer.com

Only papers with non-academic authors and company affiliations will be included.

# Tools & Libraries Used
spaCy: NLP library used for Named Entity Recognition
typer: CLI framework based on Click
lxml: XML parsing
pandas: DataFrame handling & CSV export
NCBI E-utilities API: To fetch PubMed articles

# Notes
If no non-academic authors or company affiliations are found, the tool will skip that article.
Logging is enabled for debugging and helps track article-level extraction decisions.
You can enhance classification accuracy by expanding the INDUSTRY_KEYWORDS in affiliation_classifier.py.

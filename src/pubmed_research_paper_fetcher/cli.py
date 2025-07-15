import typer
import logging
from typing import Optional
import pandas as pd

from .fetcher import fetch_pubmed_data
from .filters import extract_info

# Typer app instance
app = typer.Typer()

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.command()
def get_papers_list(
    query: str = typer.Option(..., "--query", "-q", help="Query string for PubMed"),
    file: str = typer.Option(..., "--file", "-f", help="Output CSV filename"),
    debug: Optional[bool] = typer.Option(False, "--debug", help="Enable debug logging")
):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled.")

    logger.debug(f"Query: {query}")
    logger.debug(f"File argument received: {file} (type: {type(file)})")

    # Fetch articles
    articles = fetch_pubmed_data(query)
    logger.info(f"Found {len(articles)} PubMed IDs")

    # Extract and filter info
    data = []
    for article in articles:
        result = extract_info(article)
        if result is None:
            continue
        pmid, title, pub_date, non_acad_authors, company_affiliations, email = result
        if non_acad_authors and company_affiliations:
            data.append(result)
        else:
            logger.debug(f"Skipped article PMID {pmid} due to missing non-academic authors or company affiliations.")

    if not data:
        logger.warning("No articles with non-academic authors and company affiliations were found.")
        return

    # Save to CSV
    df = pd.DataFrame(data, columns=[
        "PMID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ])
    df.to_csv(file, index=False)
    logger.info(f"CSV saved to: {file}")

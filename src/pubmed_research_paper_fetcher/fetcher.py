import requests
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
MAX_RESULTS = 100  # Adjust this number if you want more or fewer results

def fetch_pubmed_data(query: str):
    """
    Fetches PubMed article metadata using E-utilities.
    """
    # Step 1: ESearch to get PMIDs
    search_url = f"{BASE_URL}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": MAX_RESULTS,
        "retmode": "json"
    }

    logger.debug("Sending ESearch request...")
    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        logger.error("ESearch request failed")
        return []

    pmids = response.json()["esearchresult"]["idlist"]
    logger.debug(f"Retrieved PMIDs: {pmids}")

    if not pmids:
        logger.warning("No articles found for the given query.")
        return []

    # Step 2: EFetch to get article details
    fetch_url = f"{BASE_URL}/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    logger.debug("Sending EFetch request...")
    fetch_response = requests.get(fetch_url, params=fetch_params)
    if fetch_response.status_code != 200:
        logger.error("EFetch request failed")
        return []

    root = ET.fromstring(fetch_response.content)
    articles = root.findall(".//PubmedArticle")

    logger.info(f"Fetched {len(articles)} articles from PubMed.")
    return articles

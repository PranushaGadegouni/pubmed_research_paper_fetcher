from typing import Tuple, List
import re
import xml.etree.ElementTree as ET
from .utils import is_non_academic
import logging

logger = logging.getLogger(__name__)

def extract_info(article: ET.Element) -> Tuple[str, str, str, List[str], List[str], str] | None:
    pmid = article.findtext(".//PMID") or ""
    title = article.findtext(".//ArticleTitle") or ""

    pub_date = article.find(".//PubDate")
    if pub_date is not None:
        year = pub_date.findtext("Year") or ""
        month = pub_date.findtext("Month") or ""
        day = pub_date.findtext("Day") or ""
        publication_date = f"{year}-{month}-{day}".strip("-")
    else:
        publication_date = ""

    non_academic_authors = []
    company_affiliations = []
    corresponding_author_email = ""

    for author in article.findall(".//Author"):
        aff_node = author.find(".//AffiliationInfo/Affiliation")
        if aff_node is None or not aff_node.text:
            continue
        affiliation = aff_node.text.strip()

        if is_non_academic(affiliation):
            first_name = author.findtext("ForeName") or ""
            last_name = author.findtext("LastName") or ""
            full_name = f"{first_name} {last_name}".strip()

            non_academic_authors.append(full_name)
            company_affiliations.append(affiliation)

            if not corresponding_author_email:
                match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", affiliation)
                if match:
                    corresponding_author_email = match.group(0)
                else:
                    logger.warning(f"No email found in affiliation: {affiliation}")

    if not non_academic_authors:
        return None

    return (
        pmid,
        title,
        publication_date,
        non_academic_authors,
        company_affiliations,
        corresponding_author_email,
    )

"""arXiv API collector for embodied AI and robotics papers."""

from __future__ import annotations

import logging
from urllib.parse import quote_plus

import feedparser

from intel_hub.config import DATA_DIR, MAX_ITEMS_PER_SOURCE, PAPER_KEYWORDS
from intel_hub.storage import save_merged

logger = logging.getLogger(__name__)

ARXIV_API = "https://export.arxiv.org/api/query"


def _paper_from_entry(entry: object) -> dict[str, object]:
    links = getattr(entry, "links", [])
    pdf_url = next((link.get("href") for link in links if link.get("type") == "application/pdf"), "")
    return {
        "title": " ".join(str(getattr(entry, "title", "")).split()),
        "authors": [author.get("name", "") for author in getattr(entry, "authors", [])],
        "published": str(getattr(entry, "published", ""))[:10],
        "summary": " ".join(str(getattr(entry, "summary", "")).split()),
        "pdf_url": pdf_url,
    }


def collect() -> list[dict[str, object]]:
    query = " OR ".join(f'all:"{keyword}"' for keyword in PAPER_KEYWORDS)
    url = (
        f"{ARXIV_API}?search_query={quote_plus(query)}"
        f"&start=0&max_results={MAX_ITEMS_PER_SOURCE * 3}&sortBy=submittedDate&sortOrder=descending"
    )
    feed = feedparser.parse(url)
    if getattr(feed, "bozo", False):
        logger.warning("arXiv parse warning: %s", getattr(feed, "bozo_exception", "unknown"))
    records = [_paper_from_entry(entry) for entry in feed.entries]
    records = [record for record in records if record["title"] and record["pdf_url"]]
    return save_merged(DATA_DIR / "papers.json", records, key="pdf_url", date_key="published")


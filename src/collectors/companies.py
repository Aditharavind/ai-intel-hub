"""New company signal collector."""

from __future__ import annotations

from urllib.parse import quote_plus

from intel_hub.config import DATA_DIR
from intel_hub.storage import save_merged

from .rss import collect_feed


QUERIES = [
    '"physical ai" startup',
    '"embodied ai" startup',
    '"robotics foundation model" startup',
    '"humanoid robot" startup',
    '"vision language action" startup',
]


def collect() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for query in QUERIES:
        feed_url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
        for item in collect_feed(feed_url, "Google News"):
            records.append(
                {
                    "company": "",
                    "category": query.replace('"', ""),
                    "date": item["date"],
                    "source": item["url"],
                    "title": item["title"],
                    "summary": item["summary"],
                }
            )
    return save_merged(DATA_DIR / "companies.json", records, key="source")


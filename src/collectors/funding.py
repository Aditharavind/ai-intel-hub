"""Funding announcement collector using RSS/search feeds."""

from __future__ import annotations

from urllib.parse import quote_plus

from intel_hub.config import DATA_DIR, PHYSICAL_AI_COMPANIES
from intel_hub.storage import save_merged

from .rss import collect_feed


def collect() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for company in PHYSICAL_AI_COMPANIES:
        query = quote_plus(f'"{company}" funding OR raises OR valuation')
        feed_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        for item in collect_feed(feed_url, "Google News"):
            records.append(
                {
                    "company": company,
                    "round": "",
                    "amount": "",
                    "investors": [],
                    "date": item["date"],
                    "source": item["url"],
                    "title": item["title"],
                }
            )
    return save_merged(DATA_DIR / "funding.json", records, key="source")


"""Robotics news collector."""

from __future__ import annotations

from intel_hub.config import DATA_DIR, PHYSICAL_AI_COMPANIES, ROBOTICS_NEWS_FEEDS
from intel_hub.storage import save_merged

from .rss import collect_feeds


def collect_robotics_news() -> list[dict[str, str]]:
    records = collect_feeds(ROBOTICS_NEWS_FEEDS)
    return save_merged(DATA_DIR / "robotics_news.json", records, key="url")


def collect_physical_ai_news() -> list[dict[str, str]]:
    terms = tuple(term.lower() for term in PHYSICAL_AI_COMPANIES)
    records = [
        record
        for record in collect_feeds(ROBOTICS_NEWS_FEEDS)
        if any(term in f"{record.get('title', '')} {record.get('summary', '')}".lower() for term in terms)
    ]
    return save_merged(DATA_DIR / "physical_ai_news.json", records, key="url")


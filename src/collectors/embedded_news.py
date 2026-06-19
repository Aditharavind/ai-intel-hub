"""Embedded systems / microcontroller / chips news collector."""

from __future__ import annotations

from intel_hub.config import DATA_DIR, EMBEDDED_NEWS_FEEDS
from intel_hub.storage import save_fresh

from .rss import collect_feeds


def collect() -> list[dict[str, str]]:
    records = collect_feeds(EMBEDDED_NEWS_FEEDS)
    return save_fresh(DATA_DIR / "embedded_news.json", records, key="url")

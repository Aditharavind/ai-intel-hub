"""AI news collector."""

from __future__ import annotations

from intel_hub.config import AI_NEWS_FEEDS, DATA_DIR
from intel_hub.storage import save_fresh

from .rss import collect_feeds


def collect() -> list[dict[str, str]]:
    records = collect_feeds(AI_NEWS_FEEDS)
    return save_fresh(DATA_DIR / "ai_news.json", records, key="url")


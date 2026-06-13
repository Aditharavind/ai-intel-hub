"""RSS collection helpers."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import feedparser

from intel_hub.config import MAX_ITEMS_PER_SOURCE

logger = logging.getLogger(__name__)


def parse_date(entry: Any) -> str:
    value = entry.get("published") or entry.get("updated") or entry.get("created")
    if not value:
        return datetime.now(timezone.utc).date().isoformat()
    try:
        return parsedate_to_datetime(value).date().isoformat()
    except (TypeError, ValueError):
        return str(value)[:10]


def collect_feed(feed_url: str, source: str, *, limit: int = MAX_ITEMS_PER_SOURCE) -> list[dict[str, str]]:
    feed = feedparser.parse(feed_url)
    if getattr(feed, "bozo", False):
        logger.warning("Feed parse warning for %s: %s", source, getattr(feed, "bozo_exception", "unknown"))
    records: list[dict[str, str]] = []
    for entry in feed.entries[:limit]:
        records.append(
            {
                "title": str(entry.get("title", "")).strip(),
                "source": source,
                "date": parse_date(entry),
                "url": str(entry.get("link", "")).strip(),
                "summary": str(entry.get("summary", entry.get("description", ""))).strip(),
            }
        )
    return [record for record in records if record["title"] and record["url"]]


def collect_feeds(feeds: dict[str, str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for source, url in feeds.items():
        try:
            records.extend(collect_feed(url, source))
        except Exception:
            logger.exception("Failed to collect RSS feed for %s", source)
    return records


"""GitHub repository collector."""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone

from intel_hub.config import DATA_DIR, GITHUB_TOPICS, MAX_ITEMS_PER_SOURCE
from intel_hub.http import create_session, get_json
from intel_hub.scoring import trending_score
from intel_hub.storage import save_merged

logger = logging.getLogger(__name__)


def collect() -> list[dict[str, object]]:
    session = create_session()
    token = os.getenv("GITHUB_TOKEN")
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})

    since = (datetime.now(timezone.utc) - timedelta(days=30)).date().isoformat()
    records: list[dict[str, object]] = []
    for topic in GITHUB_TOPICS:
        query = f"topic:{topic} pushed:>={since}"
        try:
            payload = get_json(
                session,
                "https://api.github.com/search/repositories",
                params={"q": query, "sort": "stars", "order": "desc", "per_page": MAX_ITEMS_PER_SOURCE},
            )
        except Exception:
            logger.exception("Failed to search GitHub topic %s", topic)
            continue

        for item in payload.get("items", []):
            stars = int(item.get("stargazers_count") or 0)
            records.append(
                {
                    "repo": item.get("full_name", ""),
                    "stars": stars,
                    "language": item.get("language") or "",
                    "description": item.get("description") or "",
                    "url": item.get("html_url", ""),
                    "date": item.get("pushed_at", "")[:10],
                    "topic": topic,
                    "score": trending_score(stars_growth=stars, recent_activity=1),
                }
            )
    return save_merged(DATA_DIR / "github_repos.json", records, key="url")


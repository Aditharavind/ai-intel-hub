"""Hugging Face model collector."""

from __future__ import annotations

import logging

from intel_hub.config import DATA_DIR, HUGGINGFACE_KEYWORDS, MAX_ITEMS_PER_SOURCE
from intel_hub.http import create_session, get_json
from intel_hub.scoring import trending_score
from intel_hub.storage import save_merged

logger = logging.getLogger(__name__)


def collect() -> list[dict[str, object]]:
    session = create_session()
    records: list[dict[str, object]] = []
    for keyword in HUGGINGFACE_KEYWORDS:
        try:
            payload = get_json(
                session,
                "https://huggingface.co/api/models",
                params={
                    "search": keyword,
                    "sort": "lastModified",
                    "direction": "-1",
                    "limit": MAX_ITEMS_PER_SOURCE,
                    "full": "true",
                },
            )
        except Exception:
            logger.exception("Failed to search Hugging Face models for %s", keyword)
            continue
        for item in payload:
            model = item.get("modelId") or item.get("id", "")
            downloads = int(item.get("downloads") or 0)
            likes = int(item.get("likes") or 0)
            records.append(
                {
                    "model": model,
                    "downloads": downloads,
                    "likes": likes,
                    "url": f"https://huggingface.co/{model}",
                    "date": str(item.get("lastModified", ""))[:10],
                    "keyword": keyword,
                    "score": trending_score(downloads_growth=downloads, mentions=likes, recent_activity=1),
                }
            )
    return save_merged(DATA_DIR / "huggingface_models.json", records, key="url")


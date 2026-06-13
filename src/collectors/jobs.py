"""Greenhouse and Lever job collector."""

from __future__ import annotations

import logging

from intel_hub.config import DATA_DIR, JOB_COMPANIES, JOB_KEYWORDS
from intel_hub.http import create_session, get_json
from intel_hub.storage import save_merged

logger = logging.getLogger(__name__)


def _matches(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in JOB_KEYWORDS)


def _greenhouse(session: object, company: str, board: str) -> list[dict[str, str]]:
    payload = get_json(session, f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs", params={"content": "true"})
    records: list[dict[str, str]] = []
    for job in payload.get("jobs", []):
        text = f"{job.get('title', '')} {job.get('content', '')}"
        if _matches(text):
            records.append(
                {
                    "title": job.get("title", ""),
                    "company": company,
                    "location": (job.get("location") or {}).get("name", ""),
                    "url": job.get("absolute_url", ""),
                    "posted": str(job.get("updated_at", ""))[:10],
                }
            )
    return records


def _lever(session: object, company: str, board: str) -> list[dict[str, str]]:
    payload = get_json(session, f"https://api.lever.co/v0/postings/{board}", params={"mode": "json"})
    records: list[dict[str, str]] = []
    for job in payload:
        text = f"{job.get('text', '')} {job.get('descriptionPlain', '')}"
        if _matches(text):
            categories = job.get("categories") or {}
            records.append(
                {
                    "title": job.get("text", ""),
                    "company": company,
                    "location": categories.get("location", ""),
                    "url": job.get("hostedUrl", ""),
                    "posted": str(job.get("createdAt", "")),
                }
            )
    return records


def collect() -> list[dict[str, str]]:
    session = create_session()
    records: list[dict[str, str]] = []
    for company, boards in JOB_COMPANIES.items():
        try:
            if boards.get("greenhouse"):
                records.extend(_greenhouse(session, company, boards["greenhouse"]))
            if boards.get("lever"):
                records.extend(_lever(session, company, boards["lever"]))
        except Exception:
            logger.exception("Failed to collect jobs for %s", company)
    return save_merged(DATA_DIR / "jobs.json", records, key="url", date_key="posted")


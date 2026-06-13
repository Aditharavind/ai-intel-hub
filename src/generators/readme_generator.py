"""Markdown README and weekly report generators."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from intel_hub.config import DATA_DIR, REPORTS_DIR, ROOT_DIR
from intel_hub.storage import read_json


def _table(records: list[dict[str, Any]], columns: list[tuple[str, str]], limit: int = 10) -> str:
    if not records:
        return "_No items collected yet._\n"
    header = "| " + " | ".join(label for label, _ in columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = []
    for record in records[:limit]:
        values = []
        for _, key in columns:
            value = record.get(key, "")
            if key in {"url", "pdf_url", "source"} and isinstance(value, str) and value.startswith("http"):
                value = f"[link]({value})"
            values.append(str(value).replace("\n", " "))
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *rows]) + "\n"


def _load(name: str) -> list[dict[str, Any]]:
    return read_json(DATA_DIR / name)


def generate_readme() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections = [
        "# Physical AI Intelligence Hub",
        "",
        f"Last Updated: {now}",
        "",
        "A continuously updating intelligence feed for AI, physical AI, robotics, VLA models, world models, startups, funding, jobs, GitHub repositories, Hugging Face models, and research papers.",
        "",
        "## Latest AI News",
        _table(_load("ai_news.json"), [("Date", "date"), ("Title", "title"), ("Source", "source"), ("URL", "url")]),
        "## Physical AI News",
        _table(_load("physical_ai_news.json"), [("Date", "date"), ("Title", "title"), ("Source", "source"), ("URL", "url")]),
        "## Robotics News",
        _table(_load("robotics_news.json"), [("Date", "date"), ("Title", "title"), ("Source", "source"), ("URL", "url")]),
        "## New Research Papers",
        _table(_load("papers.json"), [("Published", "published"), ("Title", "title"), ("PDF", "pdf_url")]),
        "## New Hugging Face Models",
        _table(_load("huggingface_models.json"), [("Date", "date"), ("Model", "model"), ("Downloads", "downloads"), ("Likes", "likes"), ("URL", "url")]),
        "## Trending GitHub Repositories",
        _table(_load("github_repos.json"), [("Repo", "repo"), ("Stars", "stars"), ("Language", "language"), ("Score", "score"), ("URL", "url")]),
        "## Startup Funding",
        _table(_load("funding.json"), [("Date", "date"), ("Company", "company"), ("Round", "round"), ("Amount", "amount"), ("Source", "source")]),
        "## New Companies",
        _table(_load("companies.json"), [("Date", "date"), ("Signal", "title"), ("Category", "category"), ("Source", "source")]),
        "## Jobs",
        _table(_load("jobs.json"), [("Posted", "posted"), ("Title", "title"), ("Company", "company"), ("Location", "location"), ("URL", "url")]),
        "## Automation",
        "",
        "GitHub Actions runs `src/main.py` every 6 hours, refreshes JSON stores, regenerates this README, writes a weekly report, builds `dashboard.html`, and commits only when files changed.",
        "",
    ]
    (ROOT_DIR / "README.md").write_text("\n".join(sections), encoding="utf-8")


def generate_weekly_report() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    repos = sorted(_load("github_repos.json"), key=lambda item: item.get("score", 0), reverse=True)
    models = sorted(_load("huggingface_models.json"), key=lambda item: item.get("score", 0), reverse=True)
    funding = _load("funding.json")
    papers = _load("papers.json")
    companies = _load("companies.json")
    content = [
        "# Weekly Physical AI Intelligence Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Top Papers",
        _table(papers, [("Published", "published"), ("Title", "title"), ("PDF", "pdf_url")], limit=5),
        "## Top Repos",
        _table(repos, [("Repo", "repo"), ("Stars", "stars"), ("Score", "score"), ("URL", "url")], limit=5),
        "## Top Models",
        _table(models, [("Model", "model"), ("Downloads", "downloads"), ("Score", "score"), ("URL", "url")], limit=5),
        "## Top Funding Rounds",
        _table(funding, [("Date", "date"), ("Company", "company"), ("Amount", "amount"), ("Source", "source")], limit=5),
        "## Most Active Companies",
        _table(companies, [("Date", "date"), ("Signal", "title"), ("Category", "category"), ("Source", "source")], limit=5),
    ]
    (REPORTS_DIR / "weekly_report.md").write_text("\n".join(content), encoding="utf-8")

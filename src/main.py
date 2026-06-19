"""Run all collectors and regenerate published artifacts."""

from __future__ import annotations

import logging
from collections.abc import Callable

from collectors import ai_news, arxiv, companies, embedded_news, funding, github_trending, huggingface_models, jobs, robotics_news
from generators.dashboard_generator import generate_dashboard
from generators.readme_generator import generate_readme, generate_weekly_report

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


Collector = Callable[[], list[dict[str, object]]]


def run_collector(name: str, collector: Collector) -> None:
    try:
        records = collector()
        logger.info("%s collected %s records", name, len(records))
    except Exception:
        logger.exception("%s failed", name)


def main() -> None:
    collectors: list[tuple[str, Collector]] = [
        ("ai_news", ai_news.collect),
        ("robotics_news", robotics_news.collect_robotics_news),
        ("physical_ai_news", robotics_news.collect_physical_ai_news),
        ("embedded_news", embedded_news.collect),
        ("papers", arxiv.collect),
        ("github_repos", github_trending.collect),
        ("huggingface_models", huggingface_models.collect),
        ("funding", funding.collect),
        ("companies", companies.collect),
        ("jobs", jobs.collect),
    ]
    for name, collector in collectors:
        run_collector(name, collector)
    generate_readme()
    generate_weekly_report()
    generate_dashboard()
    logger.info("Generated README.md, reports/weekly_report.md, and index.html")


if __name__ == "__main__":
    main()


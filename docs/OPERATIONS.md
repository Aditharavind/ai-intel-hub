# Operations Guide

## Local Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python src/main.py
```

## Automation

The workflow in `.github/workflows/update.yml` runs every 6 hours and can also be started manually from the GitHub Actions tab. It installs dependencies, runs all collectors, regenerates `README.md`, `dashboard.html`, and `reports/weekly_report.md`, then commits only when files changed.

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `GITHUB_TOKEN` | Provided automatically by GitHub Actions for repository search rate limits. |
| `INTEL_HUB_USER_AGENT` | Overrides the default HTTP user agent. |
| `INTEL_HUB_TIMEOUT` | Request timeout in seconds. |
| `INTEL_HUB_MAX_ITEMS_PER_SOURCE` | Per-source collection limit. |
| `INTEL_HUB_MAX_STORED_ITEMS` | Maximum retained records per JSON store. |

## Data Files

Each collector writes a JSON list under `data/`. Existing and incoming records are merged by stable URL-like keys so repeated scheduled runs do not create duplicates. Generated Markdown and HTML outputs should be treated as build artifacts derived from those JSON stores.

## Source Strategy

The project prefers APIs and RSS feeds over HTML scraping:

- RSS for AI, robotics, physical AI, funding, and company signals.
- GitHub Search API for repositories.
- Hugging Face model API for model releases.
- arXiv API for papers.
- Greenhouse and Lever APIs for jobs.

## Extending

Add a collector as a pure `collect() -> list[dict[str, object]]` function, save through `intel_hub.storage.save_merged`, and register it in `src/main.py`. Keep failures isolated so one unavailable source does not block the whole update.


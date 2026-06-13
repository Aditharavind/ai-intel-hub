"""HTTP helpers with retries and lightweight rate-limit handling."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import REQUEST_TIMEOUT_SECONDS, USER_AGENT

logger = logging.getLogger(__name__)


def create_session() -> requests.Session:
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "HEAD"),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json, */*"})
    return session


def get_json(session: requests.Session, url: str, **kwargs: Any) -> Any:
    response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS, **kwargs)
    if response.status_code == 403 and response.headers.get("x-ratelimit-reset"):
        reset_at = int(response.headers["x-ratelimit-reset"])
        wait_seconds = max(0, min(reset_at - int(time.time()), 60))
        logger.warning("Rate limited by %s; waiting %s seconds", url, wait_seconds)
        time.sleep(wait_seconds)
        response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS, **kwargs)
    response.raise_for_status()
    return response.json()


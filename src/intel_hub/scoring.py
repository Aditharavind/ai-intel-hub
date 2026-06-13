"""Trending score helpers."""

from __future__ import annotations


def trending_score(
    *,
    stars_growth: float = 0,
    downloads_growth: float = 0,
    mentions: float = 0,
    recent_activity: float = 0,
) -> float:
    score = (
        (stars_growth * 0.4)
        + (downloads_growth * 0.3)
        + (mentions * 0.2)
        + (recent_activity * 0.1)
    )
    return round(score, 2)


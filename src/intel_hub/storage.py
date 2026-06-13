"""JSON storage helpers used by collectors."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .config import MAX_STORED_ITEMS


def read_json(path: Path, default: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return [] if default is None else default
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")
    return data


def write_json(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = list(records)
    with path.open("w", encoding="utf-8") as file:
        json.dump(normalized, file, ensure_ascii=False, indent=2)
        file.write("\n")


def merge_records(
    existing: Iterable[dict[str, Any]],
    incoming: Iterable[dict[str, Any]],
    *,
    key: str,
    date_key: str | None = "date",
    limit: int = MAX_STORED_ITEMS,
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for record in existing:
        value = record.get(key)
        if value:
            merged[str(value)] = record
    for record in incoming:
        value = record.get(key)
        if value:
            merged[str(value)] = {**merged.get(str(value), {}), **record}
    records = list(merged.values())
    if date_key:
        records.sort(key=lambda item: str(item.get(date_key, "")), reverse=True)
    return records[:limit]


def save_merged(
    path: Path,
    incoming: Iterable[dict[str, Any]],
    *,
    key: str,
    date_key: str | None = "date",
    limit: int = MAX_STORED_ITEMS,
) -> list[dict[str, Any]]:
    records = merge_records(read_json(path), incoming, key=key, date_key=date_key, limit=limit)
    write_json(path, records)
    return records


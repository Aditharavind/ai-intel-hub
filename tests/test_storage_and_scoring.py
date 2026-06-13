import unittest

from intel_hub.scoring import trending_score
from intel_hub.storage import merge_records


class StorageAndScoringTests(unittest.TestCase):
    def test_trending_score_uses_configured_weights(self) -> None:
        self.assertEqual(trending_score(stars_growth=10, downloads_growth=20, mentions=30, recent_activity=40), 20.0)

    def test_merge_records_deduplicates_and_prefers_incoming_values(self) -> None:
        existing = [{"url": "https://example.com/a", "title": "Old", "date": "2026-01-01"}]
        incoming = [{"url": "https://example.com/a", "title": "New", "date": "2026-06-12"}]

        records = merge_records(existing, incoming, key="url")

        self.assertEqual(records, [{"url": "https://example.com/a", "title": "New", "date": "2026-06-12"}])

    def test_merge_records_sorts_newest_first(self) -> None:
        records = merge_records(
            [],
            [
                {"url": "https://example.com/old", "date": "2026-01-01"},
                {"url": "https://example.com/new", "date": "2026-06-12"},
            ],
            key="url",
        )

        self.assertEqual([record["url"] for record in records], ["https://example.com/new", "https://example.com/old"])


if __name__ == "__main__":
    unittest.main()

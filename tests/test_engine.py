from datetime import datetime, timezone

import pytest

from time_traveller.dates import in_range, parse_range
from time_traveller.similarity import pick_seeds, rank_candidates, select


def track(i, artist="A", added="2021-01-01T00:00:00Z"):
    return {"id": f"id{i}", "uri": f"uri{i}", "name": f"song{i}", "artists": [artist],
            "artist_ids": [artist], "added_at": added}


def test_range_month_formats_inclusive():
    start, end = parse_range("07-2021", "01-2022")
    assert start == datetime(2021, 7, 1, tzinfo=timezone.utc)
    assert in_range("2022-01-31T23:00:00Z", start, end)
    assert not in_range("2022-02-01T00:00:00Z", start, end)
    assert not in_range("2021-06-30T23:59:59Z", start, end)


def test_bad_range():
    with pytest.raises(ValueError):
        parse_range("2022-01-01", "2021-01-01")


class FakeProvider:
    def __init__(self, table):
        self.table = table

    def similar(self, seed, limit=20):
        return self.table[seed["name"]]


def test_ranking_and_selection():
    seeds, counts = pick_seeds([track(1), track(2, "B")], 5)
    provider = FakeProvider({
        "song1": [{"name": "x", "artist": "X", "score": 1.0}, {"name": "song2", "artist": "B", "score": 0.9},
                  {"name": "y", "artist": "X", "score": 0.5}, {"name": "z", "artist": "Z", "score": 0.4}],
        "song2": [{"name": "x", "artist": "X", "score": 0.8}],
    })
    ranked = rank_candidates(seeds, counts, provider)
    assert ranked[0]["name"] == "x" and ranked[0]["hits"] == 2 and ranked[0]["match"] == 1.0

    def resolve(c):
        return {"id": c["name"], "uri": c["name"], "name": c["name"], "artists": [c["artist"]],
                "artist_ids": [c["artist"]]}

    out = select(ranked, resolve, {"id1", "id2"}, {"a|song1", "b|song2"}, count=10, max_per_artist=1)
    names = [t["name"] for t in out]
    assert names == ["x", "z"]  # seed song2 excluded, artist X capped at 1

"""Cumulative video views must be monotone throughout the visible history."""
from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends

NOW = datetime(2026, 10, 23, 12, tzinfo=UTC)


def snapshot(video, creator, hours_ago, views, community):
    observed = NOW - timedelta(hours=hours_ago)
    return {
        "video_id": video, "creator_id": creator, "topic": "industrial_supply",
        "format": "short", "published_at": NOW - timedelta(days=1),
        "observed_at": observed, "available_at": observed + timedelta(minutes=1),
        "views": views, "community_id": community, "lineage_id": "root-" + video,
    }


def test_historical_rollback_cannot_recover_in_last_pair():
    rows = [snapshot("bad", "c1", 4, 100, "A"),
            snapshot("bad", "c1", 3, 80, "A"),
            snapshot("bad", "c1", 2, 200, "A")]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 3
    assert result["series"] == []


def test_rollback_does_not_inflate_cross_community_breadth():
    rows = [snapshot("good", "c1", 3, 10, "A"),
            snapshot("good", "c1", 2, 30, "A"),
            snapshot("bad", "c2", 3, 100, "B"),
            snapshot("bad", "c2", 2, 90, "B")]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 2
    series = result["series"][0]
    assert series["video_count"] == 1
    assert series["community_breadth"] == 1
    assert series["observed_lineage_breadth"] == 1
    assert series["view_velocity_per_video_hour"] == 20


def test_rollback_does_not_satisfy_creator_threshold():
    rows = [snapshot("good", "c1", 3, 10, "A"),
            snapshot("good", "c1", 2, 30, "A"),
            snapshot("bad", "c2", 4, 100, "B"),
            snapshot("bad", "c2", 3, 80, "B"),
            snapshot("bad", "c2", 2, 200, "B")]
    series = analyse_video_trends(rows, NOW, min_creators=2)["series"][0]
    assert series["paired_creator_count_unverified"] == 1
    assert series["status"] == "UNRESOLVED"


def test_flat_counts_are_valid_zero_growth():
    rows = [snapshot("flat", "c1", 3, 10, "A"),
            snapshot("flat", "c1", 2, 10, "A")]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 0
    assert result["series"][0]["view_velocity_per_video_hour"] == 0
    assert result["series"][0]["predictive_input"] is False

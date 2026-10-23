"""Metadata consistency is required before community and lineage aggregation."""
from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends


T = datetime(2026, 10, 23, 12, tzinfo=UTC)


def row(video, creator, minutes_ago, views, **metadata):
    return {
        "video_id": video, "creator_id": creator,
        "topic": "industrial_power_failure", "format": "short",
        "published_at": T - timedelta(days=1),
        "observed_at": T - timedelta(minutes=minutes_ago),
        "available_at": T - timedelta(minutes=minutes_ago),
        "views": views, **metadata,
    }


def test_later_missing_labels_do_not_erase_ancestry():
    result = analyse_video_trends([
        row("a", "alice", 30, 10, community_id="A", lineage_id="original"),
        row("a", "alice", 10, 40),
    ], T, min_creators=1)
    series = result["series"][0]
    assert series["community_breadth"] == 1
    assert series["observed_lineage_breadth"] == 1
    assert series["view_velocity_per_video_hour"] == 90


def test_conflicting_community_excludes_video():
    result = analyse_video_trends([
        row("a", "alice", 30, 10, community_id="A"),
        row("a", "alice", 10, 40, community_id="B"),
    ], T, min_creators=1)
    assert result["series"] == []
    assert result["rejected_records"] >= 1


def test_conflicting_lineage_excludes_video():
    result = analyse_video_trends([
        row("a", "alice", 30, 10, lineage_id="origin"),
        row("a", "alice", 10, 40, lineage_id="replacement"),
    ], T, min_creators=1)
    assert result["series"] == []
    assert result["rejected_records"] >= 1


def test_metadata_conflict_does_not_contaminate_other_video():
    result = analyse_video_trends([
        row("bad", "alice", 30, 10, community_id="A"),
        row("bad", "alice", 10, 40, community_id="B"),
        row("good", "bob", 30, 100, community_id="C"),
        row("good", "bob", 10, 130, community_id="C"),
    ], T, min_creators=1)
    assert len(result["series"]) == 1
    assert result["series"][0]["community_breadth"] == 1
    assert result["series"][0]["view_velocity_per_video_hour"] == 90


def test_missing_label_can_be_enriched_later():
    result = analyse_video_trends([
        row("a", "alice", 30, 10),
        row("a", "alice", 10, 40, community_id="A", lineage_id="source"),
    ], T, min_creators=1)
    assert result["rejected_records"] == 0
    assert result["series"][0]["community_breadth"] == 1
    assert result["series"][0]["observed_lineage_breadth"] == 1


def test_conflict_does_not_depend_on_input_order():
    rows = [
        row("a", "alice", 30, 10, community_id="A"),
        row("a", "alice", 20, 20),
        row("a", "alice", 10, 40, community_id="B"),
    ]
    for order in (rows, rows[::-1], [rows[1], rows[2], rows[0]]):
        result = analyse_video_trends(order, T, min_creators=1)
        assert result["series"] == []


def test_shared_lineage_does_not_collapse_distinct_communities():
    result = analyse_video_trends([
        row("a", "alice", 30, 10, community_id="A", lineage_id="shared"),
        row("a", "alice", 10, 20, community_id="A", lineage_id="shared"),
        row("b", "bob", 30, 10, community_id="B", lineage_id="shared"),
        row("b", "bob", 10, 20, community_id="B", lineage_id="shared"),
    ], T, min_creators=2)
    series = result["series"][0]
    assert series["community_breadth"] == 2
    assert series["observed_lineage_breadth"] == 1
    assert series["predictive_input"] is False


def test_unhashable_optional_label_is_rejected():
    result = analyse_video_trends([
        row("a", "alice", 30, 10, community_id=["A"]),
        row("a", "alice", 10, 20, community_id="A"),
    ], T, min_creators=1)
    assert result["rejected_records"] == 1
    assert result["series"][0]["view_velocity_per_video_hour"] is None

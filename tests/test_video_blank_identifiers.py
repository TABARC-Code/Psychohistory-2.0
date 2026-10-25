"""Reject empty G1 video identifiers before creator and community aggregation."""
from datetime import UTC, datetime, timedelta

import pytest

from psychohistory.g1.video_trends import analyse_video_trends


CUTOFF = datetime(2026, 10, 25, 1, tzinfo=UTC)


def snapshot(video, creator, minutes_ago, views, **overrides):
    row = {
        "video_id": video, "creator_id": creator, "topic": "non_ai_power_outage",
        "format": "short", "published_at": CUTOFF - timedelta(days=1),
        "observed_at": CUTOFF - timedelta(minutes=minutes_ago),
        "available_at": CUTOFF - timedelta(minutes=minutes_ago),
        "views": views,
    }
    row.update(overrides)
    return row


@pytest.mark.parametrize(
    ("field", "blank"),
    [
        ("video_id", " "), ("creator_id", "  "), ("topic", "\t"),
        ("community_id", " "), ("lineage_id", "\t"),
        ("community_id", ""), ("lineage_id", ""),
    ],
)
def test_blank_identifier_is_not_a_video_or_community_measurement(field, blank):
    rows = [
        snapshot("video", "creator", 30, 10, **{field: blank}),
        snapshot("video", "creator", 10, 20, **{field: blank}),
    ]
    result = analyse_video_trends(rows, CUTOFF, min_creators=1)
    assert result["series"] == []
    assert result["rejected_records"] == 2
    assert result["predictive_input"] is False


def test_whitespace_creator_names_cannot_satisfy_independent_creator_threshold():
    rows = []
    for i, creator in enumerate((" ", "  ", "   ")):
        rows.extend([
            snapshot(f"video-{i}", creator, 30, 10),
            snapshot(f"video-{i}", creator, 10, 20),
        ])
    result = analyse_video_trends(rows, CUTOFF, min_creators=3)
    assert result["series"] == []
    assert result["rejected_records"] == 6
    assert result["predictive_input"] is False


def test_valid_video_remains_after_blank_metadata_is_rejected():
    rows = [
        snapshot("bad", "alice", 30, 10, community_id=" "),
        snapshot("bad", "alice", 10, 20, community_id=" "),
        snapshot("good", "bob", 30, 10, community_id="B", lineage_id="shared"),
        snapshot("good", "bob", 10, 20, community_id="B", lineage_id="shared"),
    ]
    result = analyse_video_trends(rows, CUTOFF, min_creators=1)
    assert result["rejected_records"] == 2
    assert len(result["series"]) == 1
    series = result["series"][0]
    assert series["community_breadth"] == 1
    assert series["observed_lineage_breadth"] == 1
    assert series["predictive_input"] is False


def test_unrecorded_optional_metadata_remains_allowed():
    result = analyse_video_trends([
        snapshot("good", "alice", 30, 10),
        snapshot("good", "alice", 10, 20, community_id=None, lineage_id=None),
    ], CUTOFF, min_creators=1)
    assert result["rejected_records"] == 0
    assert len(result["series"]) == 1
    assert result["series"][0]["community_breadth"] == 0

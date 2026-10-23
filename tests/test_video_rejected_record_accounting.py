"""Snapshot-level rejection accounting for G1 video diagnostics."""
from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends


T = datetime(2026, 10, 23, 12, tzinfo=UTC)


def snapshot(video, creator, offset_minutes, views, **extra):
    observed = T + timedelta(minutes=offset_minutes)
    return {
        "video_id": video, "creator_id": creator, "topic": "non_ai_weather",
        "format": "short", "published_at": T - timedelta(days=1),
        "observed_at": observed, "available_at": observed,
        "views": views, **extra,
    }


def run(rows):
    result = analyse_video_trends(rows, T, min_creators=1)
    assert result["predictive_input"] is False
    return result


def test_conflicting_identity_rejects_every_snapshot():
    rows = [
        snapshot("v", "alice", -30, 10),
        snapshot("v", "alice", -20, 15),
        snapshot("v", "bob", -10, 20),
    ]
    result = run(rows)
    assert result["series"] == []
    assert result["rejected_records"] == 3


def test_conflicting_ancestry_rejects_every_snapshot():
    rows = [
        snapshot("v", "alice", -30, 10, community_id="A"),
        snapshot("v", "alice", -20, 15),
        snapshot("v", "alice", -10, 20, community_id="B"),
    ]
    result = run(rows)
    assert result["series"] == []
    assert result["rejected_records"] == 3


def test_timestamp_collision_rejects_every_snapshot():
    rows = [
        snapshot("v", "alice", -20, 10),
        snapshot("v", "alice", -20, 12),
        snapshot("v", "alice", -10, 20),
    ]
    result = run(rows)
    assert result["series"] == []
    assert result["rejected_records"] == 3


def test_valid_video_survives_rejection_of_another_video():
    rows = [
        snapshot("bad", "alice", -30, 10),
        snapshot("bad", "bob", -20, 20),
        snapshot("good", "carol", -30, 100),
        snapshot("good", "carol", -10, 140),
    ]
    result = run(rows)
    assert result["rejected_records"] == 2
    assert len(result["series"]) == 1
    assert result["series"][0]["view_velocity_per_video_hour"] == 120.0


def test_invalid_raw_snapshot_not_double_counted():
    rows = [
        snapshot("bad", "alice", -30, 10),
        snapshot("bad", "bob", -20, 20),
        snapshot("invalid", "carol", -10, -3),
    ]
    result = run(rows)
    assert result["rejected_records"] == 3
    assert result["series"] == []


def test_future_snapshot_excluded_not_rejected():
    rows = [
        snapshot("v", "alice", -30, 10),
        snapshot("v", "alice", 30, 20),
    ]
    result = run(rows)
    assert result["rejected_records"] == 0
    assert result["series"][0]["view_velocity_per_video_hour"] is None

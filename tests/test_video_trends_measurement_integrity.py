from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends

NOW = datetime(2026, 10, 16, tzinfo=UTC)


def row(video, creator, hours, views, exposure=None, topic="industrial"):
    return {"video_id": video, "creator_id": creator, "topic": topic,
            "format": "short", "published_at": NOW - timedelta(days=1),
            "observed_at": NOW - timedelta(hours=hours),
            "views": views, "exposure": exposure}


def test_matched_exposure():
    rows = [row("v1", "c1", 2, 100, 100), row("v1", "c1", 0, 200, 200),
            row("v2", "c2", 2, 100), row("v2", "c2", 0, 300)]
    s = analyse_video_trends(rows, NOW, min_creators=2)["series"][0]
    assert s["view_velocity_per_video_hour"] == 75
    assert s["exposure_adjusted_view_rate"] == 1
    assert s["exposure_pair_coverage_fraction"] == 0.5


def test_identity_consistency():
    rows = [row("v1", "c1", 2, 100), row("v1", "c2", 0, 200)]
    r = analyse_video_trends(rows, NOW, min_creators=1)
    assert r["rejected_records"] == 1
    assert r["series"] == []


def test_single_snapshot_not_counted_as_growth():
    rows = [row("v1", "c1", 2, 100), row("v1", "c1", 0, 200),
            row("v2", "c2", 0, 500)]
    s = analyse_video_trends(rows, NOW, min_creators=2)["series"][0]
    assert s["paired_creator_count_unverified"] == 1
    assert s["status"] == "UNRESOLVED"

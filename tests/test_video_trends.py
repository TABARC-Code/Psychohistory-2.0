from datetime import UTC, datetime, timedelta
from psychohistory.g1.video_trends import analyse_video_trends

T = datetime(2026, 10, 13, tzinfo=UTC)

def record(views, observed, **kw):
    return dict(video_id="v1", creator_id="c1", topic="solar", format="short",
                published_at=T-timedelta(days=1), observed_at=observed,
                views=views, **kw)

def test_velocity_and_no_algorithmic_claim():
    result = analyse_video_trends([record(100, T-timedelta(hours=2)),
                                   record(160, T)], T, min_creators=1)
    s = result["series"][0]
    assert s["view_velocity_per_video_hour"] == 30
    assert s["predictive_input"] is False
    assert s["algorithmic_amplification"] == "NOT_IDENTIFIABLE_FROM_PUBLIC_COUNTS"

def test_future_snapshots_do_not_leak():
    result = analyse_video_trends([record(100, T-timedelta(hours=2)),
                                   record(160, T+timedelta(hours=1))], T, min_creators=1)
    assert result["series"][0]["view_velocity_per_video_hour"] is None

def test_invalid_counts_rejected():
    result = analyse_video_trends([record(float("nan"), T), record(True, T)], T)
    assert result["rejected_records"] == 2
    assert not result["series"]

def test_duplicate_timestamps_excluded():
    result = analyse_video_trends([record(100, T), record(200, T)], T, min_creators=1)
    assert result["rejected_records"] == 2
    assert result["series"] == []

def test_short_long_separate():
    short = record(10, T)
    long = dict(short, video_id="v2", format="long")
    result = analyse_video_trends([short, long], T)
    assert {s["format"] for s in result["series"]} == {"short", "long"}

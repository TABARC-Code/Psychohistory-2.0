"""Finite G1 video aggregates must not report nonfinite rates as candidates."""
from datetime import UTC, datetime, timedelta
from math import isfinite

from psychohistory.g1.video_trends import analyse_video_trends


NOW = datetime(2026, 10, 24, 2, tzinfo=UTC)


def _pair(video, delta, exposure_delta=None, topic="industrial"):
    start = NOW - timedelta(hours=2)
    end = NOW - timedelta(hours=1)
    base = {
        "video_id": video, "creator_id": "creator-" + video,
        "topic": topic, "format": "short",
        "published_at": NOW - timedelta(days=1),
    }
    return [
        {**base, "observed_at": start, "available_at": start,
         "views": 0.0, "exposure": 0.0 if exposure_delta is not None else None},
        {**base, "observed_at": end, "available_at": end,
         "views": delta, "exposure": exposure_delta},
    ]


def test_sum_of_finite_view_deltas_cannot_publish_infinite_velocity():
    rows = [row for i in range(3) for row in _pair(f"v{i}", 1e308)]
    result = analyse_video_trends(rows, NOW)
    assert result["rejected_records"] == 0
    series = result["series"][0]
    assert series["paired_creator_count_unverified"] == 3
    assert series["status"] == "UNRESOLVED"
    assert series["numerical_integrity_status"] == "UNRESOLVED_AGGREGATE_OVERFLOW"
    assert series["view_velocity_per_video_hour"] is None
    assert series["log_view_delta"] is None
    assert series["predictive_input"] is False


def test_sum_of_finite_exposure_deltas_cannot_publish_false_zero_rate():
    rows = [row for i in range(3) for row in _pair(f"v{i}", 1.0, 1e308)]
    series = analyse_video_trends(rows, NOW)["series"][0]
    assert series["view_velocity_per_video_hour"] == 1.0
    assert series["exposure_adjusted_view_rate"] is None
    assert series["numerical_integrity_status"] == "UNRESOLVED_AGGREGATE_OVERFLOW"
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_large_valid_counts_do_not_poison_independent_topics():
    rows = [row for i in range(3) for row in _pair(f"v{i}", 1e308)]
    rows += [row for i in range(3) for row in _pair(f"good{i}", 10.0, 20.0, topic="health")]
    series = {s["topic"]: s for s in analyse_video_trends(rows, NOW)["series"]}
    assert series["industrial"]["status"] == "UNRESOLVED"
    assert series["health"]["status"] == "CANDIDATE_NOT_ADMITTED"
    assert series["health"]["numerical_integrity_status"] == "VALID"
    assert isfinite(series["health"]["view_velocity_per_video_hour"])
    assert series["health"]["view_velocity_per_video_hour"] == 10.0
    assert series["health"]["exposure_adjusted_view_rate"] == 0.5
    assert series["health"]["predictive_input"] is False


def test_finite_sum_with_overflowing_derived_rate_is_unresolved():
    # One microsecond is a valid observation interval, but the rate itself
    # can exceed binary64 even though the underlying count delta does not.
    start = NOW - timedelta(microseconds=1)
    rows = [
        {
            "video_id": "fast", "creator_id": "fast", "topic": "hardware",
            "format": "short", "published_at": NOW - timedelta(days=1),
            "observed_at": t, "available_at": t, "views": views,
        }
        for t, views in ((start, 0.0), (NOW, 1e308))
    ]
    series = analyse_video_trends(rows, NOW, min_creators=1)["series"][0]
    assert series["status"] == "UNRESOLVED"
    assert series["numerical_integrity_status"] == "UNRESOLVED_AGGREGATE_OVERFLOW"
    assert series["view_velocity_per_video_hour"] is None

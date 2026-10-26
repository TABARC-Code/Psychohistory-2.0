"""Discrete view counters must not claim unit precision beyond binary64 limits.

Binary64 can represent some integers above 2**53, but it cannot resolve
consecutive unit changes there. Large floating-point counts must not bypass
the conservative integer boundary and manufacture a propagation rate.
"""

from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends


NOW = datetime(2026, 10, 26, 20, 0, tzinfo=UTC)


def snapshot(video, hours_ago, views, *, exposure=None):
    observed = NOW - timedelta(hours=hours_ago)
    return {
        "video_id": video,
        "creator_id": "creator-" + video,
        "topic": "industrial_supply",
        "format": "short",
        "published_at": NOW - timedelta(days=1),
        "observed_at": observed,
        "available_at": observed,
        "views": views,
        "exposure": exposure,
    }


def test_large_integral_floats_do_not_bypass_discrete_count_boundary():
    rows = [
        snapshot("large", 2, float(2**53 + 2)),
        snapshot("large", 1, float(2**53 + 4)),
    ]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 0
    assert len(result["series"]) == 1
    assert result["series"][0]["status"] == "UNRESOLVED"
    assert result["series"][0]["unsafe_view_count_video_count"] == 1
    assert result["series"][0]["numerical_integrity_status"] == "UNRESOLVED_COUNT_GRANULARITY"
    assert result["predictive_input"] is False


def test_large_float_counter_cannot_contaminate_valid_video_velocity():
    rows = [
        snapshot("large", 2, float(2**53 + 2)),
        snapshot("large", 1, float(2**53 + 4)),
        snapshot("valid", 2, 10),
        snapshot("valid", 1, 14),
    ]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 0
    assert len(result["series"]) == 1
    assert result["series"][0]["status"] == "UNRESOLVED"
    assert result["series"][0]["unsafe_view_count_video_count"] == 1
    assert result["series"][0]["numerical_integrity_status"] == "UNRESOLVED_COUNT_GRANULARITY"
    assert result["series"][0]["predictive_input"] is False


def test_existing_exact_boundary_and_fractional_exposure_are_preserved():
    rows = [
        snapshot("boundary", 2, 2**53 - 1, exposure=100.5),
        snapshot("boundary", 1, float(2**53), exposure=102.5),
    ]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 0
    assert result["series"][0]["view_velocity_per_video_hour"] == 1.0
    assert result["series"][0]["exposure_adjusted_view_rate"] == 0.5
    assert result["series"][0]["predictive_input"] is False

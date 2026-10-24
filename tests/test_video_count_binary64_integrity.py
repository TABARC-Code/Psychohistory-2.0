"""Video snapshot counts must not change under mixed numeric arithmetic."""
from datetime import UTC, datetime, timedelta

import pytest

from psychohistory.g1.video_trends import analyse_video_trends


NOW = datetime(2026, 10, 24, 0, tzinfo=UTC)


def _row(video, hours, views, exposure=None):
    observed = NOW - timedelta(hours=hours)
    return {
        "video_id": video, "creator_id": "creator-" + video,
        "topic": "industrial_supply_chain", "format": "short",
        "published_at": NOW - timedelta(days=1),
        "observed_at": observed, "available_at": observed,
        "views": views, "exposure": exposure,
    }


def test_unrepresentable_integer_views_are_excluded_before_mixed_subtraction():
    # float(2**53+2) - (2**53+1) is 2.0, not the true difference 1.
    rows = [_row("v1", 2, 2**53 + 1), _row("v1", 1, float(2**53 + 2))]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 1
    assert result["series"][0]["view_velocity_per_video_hour"] is None
    assert result["series"][0]["predictive_input"] is False


def test_unrepresentable_integer_exposure_cannot_distort_adjusted_rate():
    rows = [
        _row("v1", 2, 10, 2**53 + 1),
        _row("v1", 1, 11, float(2**53 + 2)),
    ]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 1
    assert result["series"][0]["exposure_adjusted_view_rate"] is None


def test_exactly_representable_mixed_counts_keep_their_rate():
    rows = [
        _row("v1", 2, 2**53 - 1, 2**53 - 1),
        _row("v1", 1, float(2**53), float(2**53)),
    ]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 0
    series = result["series"][0]
    assert series["view_velocity_per_video_hour"] == pytest.approx(1.0)
    assert series["exposure_adjusted_view_rate"] == pytest.approx(1.0)
    assert series["predictive_input"] is False


def test_invalid_large_count_does_not_exclude_independent_valid_video():
    rows = [
        _row("bad", 2, 2**53 + 1), _row("bad", 1, 2**53 + 2),
        _row("good", 2, 10, 10), _row("good", 1, 20, 20),
    ]
    result = analyse_video_trends(rows, NOW, min_creators=1)
    assert result["rejected_records"] == 2
    assert len(result["series"]) == 1
    assert result["series"][0]["view_velocity_per_video_hour"] == 10.0

"""G1 video counts should use the same exact-binary64 boundary as other estimators."""

from datetime import UTC, datetime, timedelta

import numpy as np
import pytest

from psychohistory.g1.video_trends import analyse_video_trends


CUTOFF = datetime(2026, 10, 25, 16, tzinfo=UTC)


def snapshot(views, hours_ago, *, exposure=None):
    observed = CUTOFF - timedelta(hours=hours_ago)
    return {
        "video_id": "mill-report", "creator_id": "local-reporter",
        "topic": "industrial_supply", "format": "short",
        "published_at": CUTOFF - timedelta(days=1),
        "observed_at": observed, "available_at": observed,
        "views": views, "exposure": exposure,
    }


def test_exact_numpy_integer_views_are_not_discarded():
    rows = [snapshot(np.int64(100), 2), snapshot(np.int64(140), 1)]
    result = analyse_video_trends(rows, CUTOFF, min_creators=1)
    assert result["rejected_records"] == 0
    series = result["series"][0]
    assert series["view_velocity_per_video_hour"] == pytest.approx(40)
    assert series["status"] == "CANDIDATE_NOT_ADMITTED"
    assert series["predictive_input"] is False


def test_exact_numpy_float32_exposure_is_preserved():
    rows = [
        snapshot(np.float32(100), 2, exposure=np.float32(200)),
        snapshot(np.float32(120), 1, exposure=np.float32(300)),
    ]
    result = analyse_video_trends(rows, CUTOFF, min_creators=1)
    assert result["rejected_records"] == 0
    series = result["series"][0]
    assert series["view_velocity_per_video_hour"] == pytest.approx(20)
    assert series["exposure_adjusted_view_rate"] == pytest.approx(0.2)
    assert series["exposure_pair_coverage_fraction"] == 1
    assert series["predictive_input"] is False


def test_numpy_integer_beyond_binary64_precision_still_rejected():
    rows = [
        snapshot(np.uint64(2**53 + 1), 2),
        snapshot(np.uint64(2**53 + 2), 1),
    ]
    result = analyse_video_trends(rows, CUTOFF, min_creators=1)
    assert result["rejected_records"] == 2
    assert result["series"] == []


def test_numpy_boolean_is_not_a_view_count():
    result = analyse_video_trends(
        [snapshot(np.bool_(True), 1)], CUTOFF, min_creators=1
    )
    assert result["rejected_records"] == 1
    assert result["series"] == []

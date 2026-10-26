"""Video views are discrete counts, even when providers encode them as floats.

Fractional counts must not create a synthetic propagation rate. This does
not assert that creator independence or exposure measurement is verified.
"""
from datetime import UTC, datetime, timedelta

import numpy as np
import pytest

from psychohistory.g1.video_trends import analyse_video_trends


NOW = datetime(2026, 10, 26, tzinfo=UTC)


def snapshot(views, hours_ago, *, video="v1", exposure=None):
    observed = NOW - timedelta(hours=hours_ago)
    return {
        "video_id": video, "creator_id": "creator-" + video,
        "topic": "industrial_supply", "format": "short",
        "published_at": NOW - timedelta(days=1),
        "observed_at": observed, "available_at": observed,
        "views": views, "exposure": exposure,
    }


@pytest.mark.parametrize("fractional", [0.5, 100.25, np.float32(10.5)])
def test_fractional_view_count_cannot_generate_propagation(fractional):
    result = analyse_video_trends(
        [snapshot(fractional, 2), snapshot(fractional + 10, 1)],
        NOW, min_creators=1,
    )
    assert result["rejected_records"] == 2
    assert result["series"] == []
    assert result["predictive_input"] is False


def test_fractional_count_cannot_change_a_valid_video_velocity():
    result = analyse_video_trends(
        [snapshot(100, 2), snapshot(100.5, 1)],
        NOW, min_creators=1,
    )
    assert result["rejected_records"] == 1
    assert result["series"][0]["view_velocity_per_video_hour"] is None
    assert result["series"][0]["status"] == "UNRESOLVED"


def test_integral_float_and_numpy_counts_remain_accepted():
    result = analyse_video_trends(
        [snapshot(np.float32(100.0), 2, exposure=100.5),
         snapshot(140.0, 1, exposure=200.5)],
        NOW, min_creators=1,
    )
    assert result["rejected_records"] == 0
    series = result["series"][0]
    assert series["view_velocity_per_video_hour"] == pytest.approx(40)
    # Exposure may be a measured denominator, not a discrete view count.
    assert series["exposure_adjusted_view_rate"] == pytest.approx(0.4)
    assert series["predictive_input"] is False

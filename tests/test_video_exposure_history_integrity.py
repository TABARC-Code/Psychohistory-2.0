"""Cumulative exposure is non-negative, monotone and independently diagnostic."""
from datetime import UTC, datetime, timedelta

import pytest

from psychohistory.g1.video_trends import analyse_video_trends

NOW = datetime(2026, 10, 23, 11, tzinfo=UTC)


def history(exposures, *, video="v1", views=None):
    if views is None:
        views = [10 + 20 * i for i in range(len(exposures))]
    rows = []
    for i, (exposure, view) in enumerate(zip(exposures, views)):
        observed = NOW - timedelta(hours=len(exposures) + 1 - i)
        rows.append({
            "video_id": video, "creator_id": "creator-" + video,
            "topic": "industrial_grid_disruption", "format": "short",
            "published_at": NOW - timedelta(days=1),
            "observed_at": observed,
            "available_at": observed + timedelta(minutes=1),
            "views": view, "exposure": exposure,
        })
    return rows


def analyse(rows):
    return analyse_video_trends(rows, NOW, min_creators=1)


def test_zero_origin_is_a_valid_cumulative_measurement():
    result = analyse(history([0, 100], views=[0, 40]))
    assert result["rejected_records"] == 0
    s = result["series"][0]
    assert s["exposure_adjusted_view_rate"] == pytest.approx(0.4)
    assert s["exposure_pair_coverage_fraction"] == 1
    assert s["predictive_input"] is False


def test_zero_to_zero_is_valid_without_denominator():
    result = analyse(history([0, 0], views=[0, 0]))
    assert result["rejected_records"] == 0
    s = result["series"][0]
    assert s["exposure_adjusted_view_rate"] is None
    assert s["exposure_history_status"] == "MONOTONE_REPORTED"


def test_historical_rollback_is_not_erased_by_latest_growth():
    s = analyse(history([100, 80, 200]))["series"][0]
    assert s["view_velocity_per_video_hour"] == 20
    assert s["exposure_adjusted_view_rate"] is None
    assert s["exposure_pair_coverage_fraction"] == 0
    assert s["exposure_rollback_video_count"] == 1
    assert s["exposure_history_status"] == "CUMULATIVE_ROLLBACK"
    assert s["status"] == "UNRESOLVED"


def test_latest_rollback_withheld():
    s = analyse(history([100, 90]))["series"][0]
    assert s["exposure_rollback_video_count"] == 1
    assert s["status"] == "UNRESOLVED"


def test_known_rollback_across_missing_intermediate_exposure():
    s = analyse(history([100, None, 90]))["series"][0]
    assert s["exposure_rollback_video_count"] == 1
    assert s["exposure_adjusted_view_rate"] is None


def test_unaffected_video_still_contributes_exposure_rate():
    rows = history([100, 80, 200], video="bad") + history([0, 100], video="good")
    s = analyse(rows)["series"][0]
    assert s["exposure_adjusted_view_rate"] == pytest.approx(0.2)
    assert s["exposure_pair_coverage_fraction"] == pytest.approx(0.5)
    assert s["video_count"] == 2
    assert s["status"] == "UNRESOLVED"


def test_partial_exposure_is_not_inferred_as_rollback():
    s = analyse(history([None, 100]))["series"][0]
    assert s["exposure_rollback_video_count"] == 0
    assert s["exposure_history_status"] == "PARTIAL"


def test_valid_positive_history_preserves_existing_rate():
    s = analyse(history([50, 150]))["series"][0]
    assert s["exposure_adjusted_view_rate"] == pytest.approx(0.2)
    assert s["exposure_rollback_video_count"] == 0
    assert s["status"] == "CANDIDATE_NOT_ADMITTED"


@pytest.mark.parametrize("invalid", [-1, False, float("nan")])
def test_invalid_exposure_still_rejected(invalid):
    result = analyse(history([invalid, 100]))
    assert result["rejected_records"] == 1
    assert result["series"][0]["exposure_adjusted_view_rate"] is None

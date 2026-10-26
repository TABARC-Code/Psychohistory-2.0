"""Flat cumulative counts are not observed narrative propagation growth."""
from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends


NOW = datetime(2026, 10, 26, 20, tzinfo=UTC)


def _history(video_id, start_views, end_views):
    first = NOW - timedelta(hours=3)
    second = NOW - timedelta(hours=1)
    common = {
        "video_id": video_id,
        "creator_id": "creator-" + video_id,
        "topic": "industrial_disruption",
        "format": "short",
        "published_at": NOW - timedelta(days=2),
    }
    return [
        {**common, "observed_at": first, "available_at": first,
         "views": start_views},
        {**common, "observed_at": second, "available_at": second,
         "views": end_views},
    ]


def test_three_independent_flat_histories_are_not_a_growth_candidate():
    rows = [row for index in range(3)
            for row in _history(f"video-{index}", 100, 100)]
    result = analyse_video_trends(rows, NOW)
    series = result["series"][0]
    assert series["paired_creator_count_unverified"] == 3
    assert series["view_velocity_per_video_hour"] == 0.0
    assert series["log_view_delta"] == 0.0
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_positive_observed_growth_retains_nonadmitted_candidate_status():
    rows = [row for index in range(3)
            for row in _history(f"video-{index}", 100, 120)]
    series = analyse_video_trends(rows, NOW)["series"][0]
    assert series["view_velocity_per_video_hour"] == 10.0
    assert series["status"] == "CANDIDATE_NOT_ADMITTED"
    assert series["predictive_input"] is False

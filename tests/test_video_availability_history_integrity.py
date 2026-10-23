"""Availability chronology must be checked over the full visible history."""
from datetime import UTC, datetime, timedelta, timezone

from psychohistory.g1.video_trends import analyse_video_trends

NOW = datetime(2026, 10, 23, 12, tzinfo=UTC)


def snapshot(hours_ago, views, available):
    observed = NOW - timedelta(hours=hours_ago)
    row = {"video_id": "v", "creator_id": "c", "topic": "environmental",
           "format": "short", "published_at": NOW - timedelta(days=2),
           "observed_at": observed, "views": views}
    if available is not None:
        row["available_at"] = available
    return row


def test_historical_inversion_not_erased_by_last_ordered_pair():
    rows = [snapshot(4, 10, NOW - timedelta(hours=2)),
            snapshot(3, 20, NOW - timedelta(hours=2, minutes=30)),
            snapshot(2, 30, NOW - timedelta(hours=1))]
    series = analyse_video_trends(rows, NOW, min_creators=1)["series"][0]
    assert series["out_of_order_availability_pair_count"] == 1
    assert series["availability_history_pair_coverage_fraction"] == 1
    assert series["view_velocity_per_video_hour"] == 10
    assert series["point_in_time_velocity_status"] == "UNRESOLVED_AVAILABILITY_ORDER"
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_availability_offsets_are_compared_as_utc_instants():
    plus_two = timezone(timedelta(hours=2))
    rows = [snapshot(3, 10, (NOW - timedelta(hours=2)).astimezone(plus_two)),
            snapshot(2, 20, (NOW - timedelta(hours=1)).astimezone(plus_two))]
    series = analyse_video_trends(rows, NOW, min_creators=1)["series"][0]
    assert series["out_of_order_availability_pair_count"] == 0
    assert series["point_in_time_velocity_status"] == "REPORTED_ONLY_UNVERIFIED"
    assert series["status"] == "CANDIDATE_NOT_ADMITTED"


def test_missing_history_timestamp_is_not_inferred_ordered():
    rows = [snapshot(3, 10, None),
            snapshot(2, 20, NOW - timedelta(hours=1))]
    series = analyse_video_trends(rows, NOW, min_creators=1)["series"][0]
    assert series["availability_history_pair_coverage_fraction"] == 0
    assert series["out_of_order_availability_pair_count"] == 0
    assert series["point_in_time_velocity_status"] == "UNVERIFIED_AVAILABILITY"
    assert series["predictive_input"] is False

"""Availability inversions across missing snapshot metadata remain observable."""

from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends


CUTOFF = datetime(2026, 10, 23, 12, tzinfo=UTC)


def snapshots(available_hours):
    """Cumulative snapshots in observed order; None means unavailable metadata."""
    rows = []
    for i, hour in enumerate(available_hours):
        row = {
            "video_id": "v1",
            "creator_id": "c1",
            "topic": "flood",
            "format": "short",
            "published_at": CUTOFF - timedelta(days=1),
            "observed_at": CUTOFF.replace(hour=8 + i),
            "views": 100 + 50 * i,
        }
        if hour is not None:
            row["available_at"] = CUTOFF.replace(hour=hour)
        rows.append(row)
    return rows


def test_missing_middle_does_not_hide_inversion():
    series = analyse_video_trends(snapshots([11, None, 10]), CUTOFF, min_creators=1)["series"][0]
    assert series["out_of_order_availability_pair_count"] == 1
    assert series["availability_history_pair_coverage_fraction"] == 0.0
    assert series["point_in_time_velocity_status"] == "UNRESOLVED_AVAILABILITY_ORDER"
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_inversion_across_gap_is_counted_with_adjacent_pair():
    series = analyse_video_trends(snapshots([11, None, 10, 12]), CUTOFF, min_creators=1)["series"][0]
    assert series["out_of_order_availability_pair_count"] == 1
    assert series["availability_history_pair_coverage_fraction"] == 1 / 3
    assert series["point_in_time_velocity_status"] == "UNRESOLVED_AVAILABILITY_ORDER"


def test_missing_middle_without_inversion_remains_unverified():
    series = analyse_video_trends(snapshots([10, None, 11]), CUTOFF, min_creators=1)["series"][0]
    assert series["out_of_order_availability_pair_count"] == 0
    assert series["point_in_time_velocity_status"] == "UNVERIFIED_AVAILABILITY"
    assert series["predictive_input"] is False

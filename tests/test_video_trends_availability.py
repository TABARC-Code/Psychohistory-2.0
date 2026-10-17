from datetime import UTC, datetime, timedelta, timezone

from psychohistory.g1.video_trends import analyse_video_trends

T = datetime(2026, 10, 17, 7, 0, tzinfo=UTC)


def row(views, observed, available=None):
    result = dict(video_id="v1", creator_id="c1", topic="energy", format="short",
                  published_at=T - timedelta(days=1), observed_at=observed,
                  views=views)
    if available is not None:
        result["available_at"] = available
    return result


def test_late_available_snapshot_not_backdated():
    rows = [row(100, T - timedelta(hours=2), T - timedelta(hours=1)),
            row(200, T - timedelta(minutes=30), T + timedelta(hours=1))]
    series = analyse_video_trends(rows, T, min_creators=1)["series"][0]
    assert series["view_velocity_per_video_hour"] is None
    assert series["status"] == "UNRESOLVED"


def test_complete_reported_availability_is_explicit():
    rows = [row(100, T - timedelta(hours=2), T - timedelta(hours=1)),
            row(200, T - timedelta(minutes=30), T)]
    series = analyse_video_trends(rows, T, min_creators=1)["series"][0]
    assert series["snapshot_availability_coverage_fraction"] == 1
    assert series["snapshot_availability_status"] == "REPORTED_COMPLETE"


def test_missing_availability_does_not_pretend_point_in_time_verified():
    rows = [row(100, T - timedelta(hours=2)), row(200, T)]
    series = analyse_video_trends(rows, T, min_creators=1)["series"][0]
    assert series["snapshot_availability_coverage_fraction"] == 0
    assert series["snapshot_availability_status"] == "UNMEASURED"
    assert series["predictive_input"] is False


def test_availability_offsets_are_compared_as_instants():
    plus_two = timezone(timedelta(hours=2))
    rows = [row(100, T - timedelta(hours=2),
                (T - timedelta(hours=1)).astimezone(plus_two)),
            row(200, T - timedelta(minutes=30),
                (T + timedelta(minutes=1)).astimezone(plus_two))]
    series = analyse_video_trends(rows, T, min_creators=1)["series"][0]
    assert series["view_velocity_per_video_hour"] is None


def test_availability_before_observation_rejected():
    rows = [row(100, T, T - timedelta(hours=1))]
    result = analyse_video_trends(rows, T)
    assert result["rejected_records"] == 1
    assert result["series"] == []

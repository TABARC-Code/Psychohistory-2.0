"""Candidate status requires a complete reported availability chain.

Retrospective velocity can be calculated from observation timestamps, but it
must not be described as a point-in-time candidate without availability data.
"""
from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends


CUTOFF = datetime(2026, 10, 25, 12, tzinfo=UTC)


def _snapshots():
    rows = []
    for creator in ("mill", "union", "supplier"):
        for hours_ago, views in ((2, 100), (1, 140)):
            observed = CUTOFF - timedelta(hours=hours_ago)
            rows.append({
                "video_id": creator + "-video",
                "creator_id": creator,
                "topic": "non_ai_industrial_disruption",
                "format": "short",
                "published_at": CUTOFF - timedelta(days=1),
                "observed_at": observed,
                "available_at": observed,
                "views": views,
            })
    return rows


def test_complete_reported_availability_remains_diagnostic_candidate():
    series = analyse_video_trends(_snapshots(), CUTOFF)["series"][0]
    assert series["status"] == "CANDIDATE_NOT_ADMITTED"
    assert series["point_in_time_velocity_status"] == "REPORTED_ONLY_UNVERIFIED"
    assert series["predictive_input"] is False


def test_missing_every_availability_timestamp_cannot_qualify_candidate():
    rows = _snapshots()
    for row in rows:
        row.pop("available_at")
    series = analyse_video_trends(rows, CUTOFF)["series"][0]
    assert series["view_velocity_per_video_hour"] == 40
    assert series["point_in_time_velocity_status"] == "UNVERIFIED_AVAILABILITY"
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_single_missing_availability_timestamp_cannot_qualify_candidate():
    rows = _snapshots()
    rows[0].pop("available_at")
    series = analyse_video_trends(rows, CUTOFF)["series"][0]
    assert series["availability_history_pair_coverage_fraction"] < 1
    assert series["point_in_time_velocity_status"] == "UNVERIFIED_AVAILABILITY"
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_known_inversion_still_blocks_candidate():
    rows = _snapshots()
    rows[1]["available_at"] = CUTOFF - timedelta(hours=2)
    # This is earlier than its own observation, so it must be rejected.
    result = analyse_video_trends(rows, CUTOFF)
    assert result["rejected_records"] == 1
    assert result["predictive_input"] is False

"""Growing-creator breadth must not be inferred from flat viewing histories.

These tests concern observed video growth, not transmission, independence
of creators, recommendation effects or predictive admission.
"""
from datetime import UTC, datetime, timedelta

from psychohistory.g1.video_trends import analyse_video_trends


CUTOFF = datetime(2026, 10, 26, 20, tzinfo=UTC)


def _rows(growing_creators, *, duplicate_growing_video=False):
    rows = []
    for creator in ("mill", "union", "supplier"):
        videos = (creator + "-1",)
        if duplicate_growing_video and creator == "mill":
            videos = ("mill-1", "mill-2", "mill-3")
        for video_id in videos:
            for hours_ago, views in ((2, 100), (1, 150 if creator in growing_creators else 100)):
                observed = CUTOFF - timedelta(hours=hours_ago)
                rows.append({
                    "video_id": video_id,
                    "creator_id": creator,
                    "topic": "industrial_disruption",
                    "format": "short",
                    "published_at": CUTOFF - timedelta(days=1),
                    "observed_at": observed,
                    "available_at": observed,
                    "views": views,
                    "community_id": creator,
                    "lineage_id": "shared_notice",
                })
    return rows


def test_flat_creators_do_not_supply_growth_breadth():
    series = analyse_video_trends(_rows({"mill"}), CUTOFF)["series"][0]
    assert series["view_velocity_per_video_hour"] > 0
    assert series["paired_creator_count_unverified"] == 3
    assert series["growing_paired_creator_count_unverified"] == 1
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_distinct_growing_creators_remain_diagnostic_candidates():
    series = analyse_video_trends(
        _rows({"mill", "union", "supplier"}), CUTOFF
    )["series"][0]
    assert series["growing_paired_creator_count_unverified"] == 3
    assert series["status"] == "CANDIDATE_NOT_ADMITTED"
    assert series["predictive_input"] is False


def test_multiple_growing_videos_from_one_creator_do_not_invent_breadth():
    series = analyse_video_trends(
        _rows({"mill"}, duplicate_growing_video=True), CUTOFF
    )["series"][0]
    assert series["paired_creator_count_unverified"] == 3
    assert series["growing_paired_creator_count_unverified"] == 1
    assert series["status"] == "UNRESOLVED"

"""Creator-count thresholds are part of the diagnostic measurement contract."""
from datetime import UTC, datetime, timedelta

import pytest

from psychohistory.g1.video_trends import analyse_video_trends


T = datetime(2026, 10, 25, 4, tzinfo=UTC)


def snapshots():
    rows = []
    for creator in ("alice", "bob"):
        for minutes, views in ((30, 100), (10, 140)):
            observed = T - timedelta(minutes=minutes)
            rows.append({
                "video_id": creator + "-video",
                "creator_id": creator,
                "topic": "non_ai_industrial_shutdown",
                "format": "short",
                "published_at": T - timedelta(days=1),
                "observed_at": observed,
                "available_at": observed,
                "views": views,
            })
    return rows


@pytest.mark.parametrize("threshold", [
    None, False, True, 0, -1, 0.0, 1.0, 1.5, "2", float("nan"), float("inf"),
])
def test_invalid_creator_threshold_rejected_before_diagnostic(threshold):
    with pytest.raises(ValueError, match="min_creators"):
        analyse_video_trends(snapshots(), T, min_creators=threshold)


def test_creator_threshold_is_not_silently_relaxed():
    rows = snapshots()
    strict = analyse_video_trends(rows, T, min_creators=3)["series"][0]
    attainable = analyse_video_trends(rows, T, min_creators=2)["series"][0]
    assert strict["status"] == "UNRESOLVED"
    assert attainable["status"] == "CANDIDATE_NOT_ADMITTED"
    assert strict["predictive_input"] is False
    assert attainable["predictive_input"] is False


def test_default_creator_threshold_remains_three():
    result = analyse_video_trends(snapshots(), T)
    assert result["series"][0]["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False

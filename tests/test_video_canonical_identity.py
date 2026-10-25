"""Canonical video identities prevent artificial creator and community breadth."""
from datetime import UTC, datetime, timedelta

import pytest

from psychohistory.g1.video_trends import analyse_video_trends


CUTOFF = datetime(2026, 10, 25, 7, tzinfo=UTC)


def snapshots(video, creator, **metadata):
    base = {
        "video_id": video, "creator_id": creator,
        "topic": "non_ai_factory_shutdown", "format": "short",
        "published_at": CUTOFF - timedelta(days=1),
    }
    base.update(metadata)
    return [
        {**base, "observed_at": CUTOFF - timedelta(minutes=30),
         "available_at": CUTOFF - timedelta(minutes=30), "views": 10},
        {**base, "observed_at": CUTOFF - timedelta(minutes=10),
         "available_at": CUTOFF - timedelta(minutes=10), "views": 20},
    ]


@pytest.mark.parametrize(("field", "padded"), [
    ("video_id", " video "), ("creator_id", " creator "),
    ("topic", " non_ai_factory_shutdown "),
    ("community_id", " A "), ("lineage_id", " root "),
])
def test_padded_identity_cannot_enter_g1_video_breadth(field, padded):
    rows = snapshots("video", "creator", **{field: padded})
    result = analyse_video_trends(rows, CUTOFF, min_creators=1)
    assert result["series"] == []
    assert result["rejected_records"] == 2
    assert result["predictive_input"] is False


def test_padded_creator_cannot_satisfy_independent_creator_threshold():
    rows = (
        snapshots("v1", "alice")
        + snapshots("v2", " alice ")
        + snapshots("v3", "bob")
    )
    result = analyse_video_trends(rows, CUTOFF, min_creators=3)
    assert result["rejected_records"] == 2
    assert len(result["series"]) == 1
    series = result["series"][0]
    assert series["independent_creator_count_unverified"] == 2
    assert series["status"] == "UNRESOLVED"
    assert series["predictive_input"] is False


def test_canonical_video_labels_preserve_valid_measurements():
    rows = snapshots("v1", "alice", community_id="A", lineage_id="root")
    result = analyse_video_trends(rows, CUTOFF, min_creators=1)
    assert result["rejected_records"] == 0
    series = result["series"][0]
    assert series["status"] == "CANDIDATE_NOT_ADMITTED"
    assert series["community_breadth"] == 1
    assert series["observed_lineage_breadth"] == 1
    assert series["predictive_input"] is False

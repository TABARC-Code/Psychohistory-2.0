"""Cross-community ancestry bounds with incomplete content metadata."""
from datetime import UTC, datetime, timedelta

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


def _event(i, community, ancestry=()):
    when = datetime(2026, 1, 1, tzinfo=UTC) + timedelta(hours=i)
    return Observation(
        f"community-bound-{i}", "g1:meme", when, when, 1.0, "source",
        ancestry=("collector",), evidence_role="propagation",
        community_id=community, content_ancestry=ancestry,
    )


def _bounds(events):
    return analyse_memetic_observations(events)["social_resonance"]


def test_one_known_community_missing_all_lineage_cannot_cross():
    r = _bounds([_event(0, "a"), _event(1, "a"), _event(2, "a")])
    assert r["community_coverage_fraction"] == 1
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 0
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 0
    assert r["cross_community_lineage_overlap_status"] == "UNMEASURED"


def test_one_known_community_partial_lineage_cannot_cross():
    r = _bounds([_event(0, "a", ("root",)), _event(1, "a")])
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 0
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 0
    assert r["cross_community_lineage_overlap_status"] == "PARTIAL"


def test_missing_community_can_hide_cross_community_overlap():
    r = _bounds([_event(0, "a", ("root",)), _event(1, None)])
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 0
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1


def test_two_known_communities_with_missing_lineage_can_hide_overlap():
    r = _bounds([_event(0, "a", ("root",)), _event(1, "b")])
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 0
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1


def test_complete_joint_metadata_preserves_exact_overlap():
    r = _bounds([_event(0, "a", ("root",)), _event(1, "b", ("root",))])
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 1
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1

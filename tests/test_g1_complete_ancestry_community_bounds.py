"""Identification bounds when content ancestry is complete but community labels are not."""

from datetime import UTC, datetime, timedelta
from itertools import product
from random import Random

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


def _event(i, community, content):
    when = datetime(2026, 1, 1, tzinfo=UTC) + timedelta(hours=i)
    return Observation(
        f"complete-ancestry-{i}", "g1:meme", when, when, 1.0, "source",
        ancestry=("collector",), evidence_role="propagation",
        community_id=community, content_ancestry=content,
    )


def _resonance(rows):
    result = analyse_memetic_observations([
        _event(i, community, content)
        for i, (community, content) in enumerate(rows)
    ])
    assert result["predictive_input"] is False
    return result["social_resonance"]


def _exact_maximum(rows):
    missing = [i for i, (community, _) in enumerate(rows) if community is None]
    best = 0.0
    # Every distinct unknown community can be represented by one of N labels.
    labels = tuple(range(len(rows)))
    for assignments in product(labels, repeat=len(missing)):
        assigned = [community for community, _ in rows]
        for i, label in zip(missing, assignments):
            assigned[i] = label
        ancestor_communities = {}
        for community, (_, content) in zip(assigned, rows):
            for ancestor in content:
                ancestor_communities.setdefault(ancestor, set()).add(community)
        cross = {
            ancestor for ancestor, communities in ancestor_communities.items()
            if len(communities) >= 2
        }
        best = max(
            best,
            sum(bool(set(content) & cross) for _, content in rows) / len(rows),
        )
    return best


def test_unique_ancestors_cannot_form_cross_community_lineage():
    rows = [("a", ("r",)), (None, ("s",))]
    r = _resonance(rows)
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 0
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 0
    assert r["cross_community_lineage_overlap_status"] == "PARTIAL"


def test_unknown_community_can_complete_only_repeated_lineage():
    rows = [("a", ("r",)), (None, ("r",)), ("b", ("s",))]
    r = _resonance(rows)
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 0
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 2 / 3


def test_existing_cross_community_lineage_cannot_absorb_singleton():
    rows = [("a", ("r",)), ("b", ("r",)), (None, ("s",))]
    r = _resonance(rows)
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 2 / 3
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 2 / 3


def test_unknown_communities_can_still_form_cross_community_lineage():
    rows = [(None, ("r",)), (None, ("r",)), ("b", ("s",))]
    r = _resonance(rows)
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 2 / 3


def test_missing_ancestry_keeps_conservative_bound():
    r = _resonance([("a", ("r",)), (None, ())])
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1


def test_complete_joint_metadata_still_exact():
    r = _resonance([("a", ("r",)), ("b", ("r",)), ("b", ("s",))])
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 2 / 3
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 2 / 3


def test_randomised_upper_bound_dominates_all_community_assignments():
    rng = Random(18401)
    options = (("r",), ("s",), ("r", "s"))
    for _ in range(160):
        rows = [
            (rng.choice(("a", "b", None)), rng.choice(options))
            for _ in range(rng.randrange(1, 5))
        ]
        r = _resonance(rows)
        lower = r["cross_community_lineage_overlap_event_fraction_lower_bound"]
        upper = r["cross_community_lineage_overlap_event_fraction_upper_bound"]
        assert 0 <= lower <= _exact_maximum(rows) <= upper <= 1

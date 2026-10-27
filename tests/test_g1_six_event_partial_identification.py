"""Six-event checks for partial G1 content lineage and community bounds.

Complete missing labels independently. These are identification tests, not
transmission estimates, source independence or predictive validation.
"""
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from itertools import permutations, product

import pytest

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


CASES = (
    (("a", ("r",)), ("a", ("t",)), ("a", ("s",)),
     ("c", ("r", "s")), ("a", ()), ("a", ("t",))),
    (("b", ("t",)), ("a", ("t",)), ("b", ()),
     (None, ("s",)), ("b", ("r",)), ("a", ("t",))),
    (("b", ()), ("a", ("s",)), ("b", ("t",)),
     ("b", ("r", "s")), (None, ("r", "s")), ("c", ("r", "s"))),
    (("a", ()), ("c", ("r", "s")), ("a", ("t",)),
     ("a", ("s",)), (None, ("s",)), ("b", ("s",))),
)

ROOTS = ("r", "s", "t", "new")
UNKNOWN_ROOT_SETS = tuple(
    tuple(root for root, present in zip(ROOTS, mask) if present)
    for mask in product((False, True), repeat=len(ROOTS))
)


def _resonance(rows):
    start = datetime(2026, 1, 1, tzinfo=UTC)
    observations = [
        Observation(
            f"event-{i}", "g1:lineage", start + timedelta(minutes=i),
            start + timedelta(minutes=i), 1.0, "source",
            ancestry=("collector",), evidence_role="propagation",
            community_id=community, content_ancestry=roots,
        )
        for i, (community, roots) in enumerate(rows)
    ]
    result = analyse_memetic_observations(observations)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["predictive_input"] is False
    return result["social_resonance"]


def _truth(rows):
    root_counts = Counter(
        root for _, roots in rows for root in set(roots)
    )
    shared = {root for root, count in root_counts.items() if count > 1}
    root_communities = defaultdict(set)
    for community, roots in rows:
        for root in set(roots):
            root_communities[root].add(community)
    cross = {
        root for root, communities in root_communities.items()
        if len(communities) > 1
    }
    return (
        sum(bool(set(roots) & shared) for _, roots in rows) / len(rows),
        sum(bool(set(roots) & cross) for _, roots in rows) / len(rows),
    )


def _completions(rows):
    communities = [
        (community,) if community is not None else ("a", "b", "c", "new")
        for community, _ in rows
    ]
    roots = [
        (ancestry,) if ancestry else UNKNOWN_ROOT_SETS
        for _, ancestry in rows
    ]
    for completed_communities in product(*communities):
        for completed_roots in product(*roots):
            yield tuple(zip(completed_communities, completed_roots))


@pytest.mark.parametrize("rows", CASES)
def test_six_event_lineage_bounds_contain_every_metadata_completion(rows):
    resonance = _resonance(rows)
    shared_lower = resonance["shared_lineage_event_fraction_lower_bound"]
    shared_upper = resonance["shared_lineage_event_fraction_upper_bound"]
    cross_lower = resonance[
        "cross_community_lineage_overlap_event_fraction_lower_bound"
    ]
    cross_upper = resonance[
        "cross_community_lineage_overlap_event_fraction_upper_bound"
    ]
    assert 0 <= shared_lower <= shared_upper <= 1
    assert 0 <= cross_lower <= cross_upper <= 1

    completed = [_truth(case) for case in _completions(rows)]
    assert len(completed) >= 16
    assert all(
        shared_lower <= shared <= shared_upper
        and cross_lower <= cross <= cross_upper
        for shared, cross in completed
    )
    # These cases deliberately have sharp cross-community bounds. Missing
    # ancestry and missing community labels cannot justify a narrower claim.
    assert cross_lower == pytest.approx(min(cross for _, cross in completed))
    assert cross_upper == pytest.approx(max(cross for _, cross in completed))


def test_six_event_partial_lineage_bounds_are_row_order_invariant():
    rows = CASES[1]
    fields = (
        "shared_lineage_event_fraction_lower_bound",
        "shared_lineage_event_fraction_upper_bound",
        "cross_community_lineage_overlap_event_fraction_lower_bound",
        "cross_community_lineage_overlap_event_fraction_upper_bound",
    )
    reference = _resonance(rows)
    for reordered in permutations(rows):
        candidate = _resonance(reordered)
        assert tuple(candidate[key] for key in fields) == tuple(
            reference[key] for key in fields
        )

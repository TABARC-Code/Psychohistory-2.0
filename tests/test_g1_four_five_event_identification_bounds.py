"""Four- and five-event checks for partial G1 lineage identification.

These are metadata-completion checks, not inferred transmission or forecasts.
Known content roots and community labels remain fixed. Missing fields are
completed independently to test whether measured bounds contain the truth.
"""

from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from itertools import permutations, product

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


def _resonance(rows):
    start = datetime(2026, 1, 1, tzinfo=UTC)
    events = [
        Observation(
            f"case-{i}", "g1:lineage", start + timedelta(minutes=i),
            start + timedelta(minutes=i), 1.0, "source",
            ancestry=("collector",), evidence_role="propagation",
            community_id=community, content_ancestry=roots,
        )
        for i, (community, roots) in enumerate(rows)
    ]
    result = analyse_memetic_observations(events)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["predictive_input"] is False
    return result["social_resonance"]


def _true_fractions(communities, ancestries):
    counts = Counter(
        root for roots in ancestries for root in set(roots)
    )
    shared = {root for root, count in counts.items() if count > 1}
    shared_fraction = sum(
        bool(set(roots) & shared) for roots in ancestries
    ) / len(ancestries)

    members = defaultdict(set)
    for community, roots in zip(communities, ancestries):
        for root in set(roots):
            members[root].add(community)
    cross = {root for root, groups in members.items() if len(groups) > 1}
    cross_fraction = sum(
        bool(set(roots) & cross) for roots in ancestries
    ) / len(ancestries)
    return shared_fraction, cross_fraction


def _completions(rows):
    # Three observed roots plus one genuinely unobserved root are sufficient
    # to stress these fixed cases; this is not an exhaustive universe of roots.
    possible_roots = ("r", "s", "t", "new")
    possible_ancestries = tuple(
        tuple(root for root, present in zip(possible_roots, mask) if present)
        for mask in product((False, True), repeat=len(possible_roots))
    )
    communities = [
        (community,) if community is not None else ("a", "b", "new")
        for community, _ in rows
    ]
    ancestries = [
        (roots,) if roots else possible_ancestries
        for _, roots in rows
    ]
    for completed_communities in product(*communities):
        for completed_ancestries in product(*ancestries):
            yield _true_fractions(completed_communities, completed_ancestries)


CASES = (
    (("a", ("r",)), ("b", ("r",)), (None, ("r",)), (None, ())),
    (("a", ("r",)), ("a", ("s",)), ("b", ()), (None, ())),
    (("a", ("r",)), ("a", ("r",)), ("b", ("s",)), (None, ())),
    (("a", ("r",)), ("b", ("s",)), (None, ()), (None, ())),
    (("a", ("r", "s")), ("b", ("s",)), (None, ("r",)), (None, ())),
    (("a", ("r",)), ("b", ("r",)), ("a", ("s",)), (None, ()), (None, ())),
    (("a", ("r",)), ("a", ("s",)), ("b", ("s",)), (None, ("r",)), (None, ())),
    (("a", ("r",)), ("a", ("r",)), ("b", ("s",)), ("b", ("s",)), (None, ())),
    (("a", ("t",)), ("a", ("r",)), ("a", ()), ("a", ()), ("a", ("s",))),
    ((None, ("r",)), (None, ("r",)), (None, ("s",)), (None, ("t",))),
)


def test_four_and_five_event_bounds_cover_adversarial_metadata_completions():
    checked = 0
    for rows in CASES:
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
        for shared, cross in _completions(rows):
            assert shared_lower <= shared <= shared_upper
            assert cross_lower <= cross <= cross_upper
            checked += 1
    assert checked >= 1000


def test_lineage_identification_bounds_do_not_depend_on_event_row_order():
    rows = CASES[0]
    keys = (
        "shared_lineage_event_fraction_lower_bound",
        "shared_lineage_event_fraction_upper_bound",
        "cross_community_lineage_overlap_event_fraction_lower_bound",
        "cross_community_lineage_overlap_event_fraction_upper_bound",
    )
    reference = _resonance(rows)
    for reordered in permutations(rows):
        actual = _resonance(reordered)
        assert tuple(actual[key] for key in keys) == tuple(
            reference[key] for key in keys
        )

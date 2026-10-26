"""Exhaustive small-sample checks of G1 lineage identification bounds.

Unknown ancestry is not an independent origin, and an unknown community
is not evidence of cross-community transmission. Enumerate plausible
completions rather than assuming missing labels are distinct.
"""

from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from itertools import product

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


def _measured_bounds(rows):
    start = datetime(2026, 1, 1, tzinfo=UTC)
    events = [
        Observation(
            f"enumerated-{i}", "g1:lineage", start + timedelta(minutes=i),
            start + timedelta(minutes=i), 1.0, "source",
            ancestry=("collector",), evidence_role="propagation",
            community_id=community, content_ancestry=ancestry,
        )
        for i, (community, ancestry) in enumerate(rows)
    ]
    result = analyse_memetic_observations(events)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["predictive_input"] is False
    return result["social_resonance"]


def _completed_fractions(communities, ancestries):
    roots = Counter(
        root for ancestry in ancestries for root in set(ancestry)
    )
    shared = {root for root, count in roots.items() if count > 1}
    shared_fraction = sum(
        bool(set(ancestry) & shared) for ancestry in ancestries
    ) / len(ancestries)

    root_communities = defaultdict(set)
    for community, ancestry in zip(communities, ancestries):
        for root in set(ancestry):
            root_communities[root].add(community)
    cross = {
        root for root, members in root_communities.items()
        if len(members) > 1
    }
    cross_fraction = sum(
        bool(set(ancestry) & cross) for ancestry in ancestries
    ) / len(ancestries)
    return shared_fraction, cross_fraction


def _exact_completion_ranges(rows):
    # Up to three observations need at most three distinct communities.
    # A single additional root can represent shared ancestry not yet recorded.
    root_choices = ("r", "s", "new")
    ancestry_choices = [
        tuple(root for root, included in zip(root_choices, bits) if included)
        for bits in product((False, True), repeat=len(root_choices))
    ]
    community_options = [
        (community,) if community is not None else ("a", "b", "new")
        for community, _ in rows
    ]
    ancestry_options = [
        (ancestry,) if ancestry else ancestry_choices
        for _, ancestry in rows
    ]

    shared_values = []
    cross_values = []
    for communities in product(*community_options):
        for ancestries in product(*ancestry_options):
            shared, cross = _completed_fractions(communities, ancestries)
            shared_values.append(shared)
            cross_values.append(cross)
    return (
        (min(shared_values), max(shared_values)),
        (min(cross_values), max(cross_values)),
    )


def test_lineage_and_cross_community_bounds_cover_all_small_completions():
    possibilities = tuple(product(
        ("a", "b", None), ((), ("r",), ("s",), ("r", "s"))
    ))
    checked = 0
    for count in (1, 2, 3):
        for rows in product(possibilities, repeat=count):
            resonance = _measured_bounds(rows)
            (shared_min, shared_max), (cross_min, cross_max) = (
                _exact_completion_ranges(rows)
            )
            shared_lower = resonance["shared_lineage_event_fraction_lower_bound"]
            shared_upper = resonance["shared_lineage_event_fraction_upper_bound"]
            cross_lower = resonance[
                "cross_community_lineage_overlap_event_fraction_lower_bound"
            ]
            cross_upper = resonance[
                "cross_community_lineage_overlap_event_fraction_upper_bound"
            ]
            assert 0 <= shared_lower <= shared_min <= shared_max <= shared_upper <= 1
            assert 0 <= cross_lower <= cross_min <= cross_max <= cross_upper <= 1
            checked += 1
    assert checked == 1884

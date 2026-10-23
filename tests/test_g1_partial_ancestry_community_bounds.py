"""Conservative G1 cross-community bounds with missing ancestry and labels."""

from datetime import UTC, datetime, timedelta
from itertools import product
from random import Random

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


def _bound(rows):
    start = datetime(2026, 1, 1, tzinfo=UTC)
    observations = [
        Observation(
            f"partial-{i}", "g1:meme", start + timedelta(minutes=i),
            start + timedelta(minutes=i), 1.0, "source",
            ancestry=("collector",), evidence_role="propagation",
            community_id=community, content_ancestry=ancestry,
        )
        for i, (community, ancestry) in enumerate(rows)
    ]
    result = analyse_memetic_observations(observations)
    assert result["predictive_input"] is False
    return result["social_resonance"][
        "cross_community_lineage_overlap_event_fraction_upper_bound"
    ]


def _exact_maximum(rows):
    # Missing ancestry is allowed to contain any subset of known roots plus
    # one shared new root. Missing community labels can take a new value.
    roots = tuple(sorted({root for _, ancestry in rows for root in ancestry} | {"new"}))
    subsets = [
        tuple(root for root, present in zip(roots, bits) if present)
        for bits in product((False, True), repeat=len(roots))
    ]
    community_choices = ("a", "b", "new")
    community_options = [
        (community,) if community is not None else community_choices
        for community, _ in rows
    ]
    ancestry_options = [
        (ancestry,) if ancestry else subsets for _, ancestry in rows
    ]
    best = 0.0
    for communities in product(*community_options):
        for ancestries in product(*ancestry_options):
            roots_to_communities = {}
            for community, ancestry in zip(communities, ancestries):
                for root in ancestry:
                    roots_to_communities.setdefault(root, set()).add(community)
            cross = {
                root for root, members in roots_to_communities.items()
                if len(members) >= 2
            }
            best = max(
                best,
                sum(bool(set(ancestry) & cross) for ancestry in ancestries)
                / len(rows),
            )
            if best == 1:
                return best
    return best


def test_missing_ancestry_cannot_create_cross_community_root_in_same_community():
    rows = [("a", ("r",)), ("a", ()), ("b", ("s",))]
    assert _bound(rows) == 2 / 3


def test_missing_ancestry_cannot_retroactively_share_unrelated_known_roots():
    rows = [("a", ("r",)), ("a", ("r",)), ("a", ()), ("b", ("s",))]
    assert _bound(rows) == 2 / 4


def test_two_missing_ancestries_in_different_communities_can_cover_all():
    rows = [("a", ("r",)), ("a", ()), ("b", ("s",)), ("b", ())]
    assert _bound(rows) == 1


def test_unknown_community_and_ancestry_preserve_uncertainty():
    assert _bound([("a", ("r",)), (None, ()), ("b", ("s",))]) == 1


def test_missing_ancestry_single_known_community_still_zero():
    assert _bound([("a", ("r",)), ("a", ()), ("a", ("s",))]) == 0


def test_random_completions_cannot_exceed_partial_metadata_upper_bound():
    rng = Random(18424)
    ancestry_options = ((), ("r",), ("s",), ("r", "s"))
    for _ in range(90):
        rows = [
            (rng.choice(("a", "b", None)), rng.choice(ancestry_options))
            for _ in range(rng.randint(2, 3))
        ]
        if sum(not ancestry for _, ancestry in rows) > 2:
            continue
        assert _exact_maximum(rows) <= _bound(rows) + 1e-12

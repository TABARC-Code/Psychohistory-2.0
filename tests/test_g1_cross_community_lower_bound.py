"""G1 lower identification bound for observed cross-community content roots."""

from datetime import UTC, datetime, timedelta
from itertools import product
from random import Random

from psychohistory.core.models import Observation
from psychohistory.g1.memetics import analyse_memetic_observations


def _resonance(rows):
    origin = datetime(2026, 1, 1, tzinfo=UTC)
    observations = [
        Observation(
            f"cross-lower-{i}", "g1:meme",
            origin + timedelta(minutes=i), origin + timedelta(minutes=i),
            1.0, "source", ancestry=("collector",),
            evidence_role="propagation", community_id=community,
            content_ancestry=ancestry,
        )
        for i, (community, ancestry) in enumerate(rows)
    ]
    result = analyse_memetic_observations(observations)
    assert result["predictive_input"] is False
    return result["social_resonance"]


def test_unlabelled_member_of_proven_cross_community_root_is_certain():
    rows = [("a", ("root",)), ("b", ("root",)), (None, ("root",))]
    resonance = _resonance(rows)
    assert resonance["cross_community_lineage_overlap_event_fraction_lower_bound"] == 1
    assert resonance["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1
    assert resonance["cross_community_lineage_overlap_status"] == "PARTIAL"


def test_unlabelled_member_counts_despite_unrelated_singleton():
    rows = [("a", ("root",)), ("b", ("root",)),
            (None, ("root",)), (None, ("unrelated",))]
    resonance = _resonance(rows)
    assert resonance["cross_community_lineage_overlap_event_fraction_lower_bound"] == 3 / 4
    assert resonance["cross_community_lineage_overlap_event_fraction_upper_bound"] == 3 / 4


def test_missing_ancestry_cannot_erase_proven_cross_root_membership():
    rows = [("a", ("root",)), ("b", ("root",)),
            (None, ("root",)), (None, ())]
    resonance = _resonance(rows)
    assert resonance["cross_community_lineage_overlap_event_fraction_lower_bound"] == 3 / 4
    assert resonance["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1


def test_unlabelled_members_do_not_invent_cross_community_roots():
    rows = [("a", ("root",)), (None, ("root",)), (None, ("other",))]
    resonance = _resonance(rows)
    assert resonance["cross_community_lineage_overlap_event_fraction_lower_bound"] == 0


def test_randomised_bounds_cover_every_missing_community_assignment():
    rng = Random(19224)
    for _ in range(120):
        rows = [
            (rng.choice(("a", "b", None)),
             rng.choice((("root",), ("other",), ("root", "other"))))
            for _ in range(rng.randint(1, 4))
        ]
        resonance = _resonance(rows)
        missing = [i for i, (community, _) in enumerate(rows) if community is None]
        exact = []
        for assigned in product(("a", "b", "c", "d"), repeat=len(missing)):
            communities = [community for community, _ in rows]
            for i, community in zip(missing, assigned):
                communities[i] = community
            root_communities = {}
            for community, (_, ancestry) in zip(communities, rows):
                for root in ancestry:
                    root_communities.setdefault(root, set()).add(community)
            cross_roots = {
                root for root, members in root_communities.items() if len(members) >= 2
            }
            exact.append(sum(bool(set(ancestry) & cross_roots)
                             for _, ancestry in rows) / len(rows))
        lower = resonance["cross_community_lineage_overlap_event_fraction_lower_bound"]
        upper = resonance["cross_community_lineage_overlap_event_fraction_upper_bound"]
        assert 0 <= lower <= min(exact) <= max(exact) <= upper <= 1

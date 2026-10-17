from datetime import UTC, datetime, timedelta
from random import Random

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


def event(i, *, community=None, content=(), collector=("collector",), variant=None):
    when = datetime(2026, 1, 1, tzinfo=UTC) + timedelta(hours=i)
    return Observation(
        f"p{i}", "g1:meme", when, when, 1.0, "source",
        ancestry=collector, evidence_role="propagation",
        content_ancestry=content, community_id=community,
        semantic_variant=variant,
    )


def test_shared_collector_is_not_shared_content_lineage():
    obs = [event(0, community="a"), event(1, community="b")]
    measured = validate_observations(obs, obs[-1].available_at)
    g1 = analyse_memetic_observations(obs)
    assert measured["shared_content_ancestry"] == {}
    assert measured["shared_propagation_measurement_ancestry"] == {"collector": 2}
    assert g1["social_resonance"]["shared_lineage_event_fraction"] == 0
    assert g1["social_resonance"]["shared_lineage_fraction_status"] == "UNMEASURED"
    assert g1["social_resonance"]["shared_lineage_event_fraction_upper_bound"] == 1
    assert g1["predictive_input"] is False


def test_cross_community_overlap_is_not_direction():
    obs = [event(0, community="a", content=("root",)),
           event(1, community="b", content=("root",))]
    forward = analyse_memetic_observations(obs)["social_resonance"]
    reverse = analyse_memetic_observations(list(reversed(obs)))["social_resonance"]
    assert forward["cross_community_content_lineages_observed"] == 1
    assert forward["cross_community_lineage_overlap_event_fraction_lower_bound"] == 1
    assert forward["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1
    assert reverse["cross_community_lineage_overlap_event_fraction_lower_bound"] == 1


def test_shared_content_within_one_community_is_not_cross_spread():
    obs = [event(0, community="a", content=("root",)),
           event(1, community="a", content=("root",))]
    r = analyse_memetic_observations(obs)["social_resonance"]
    assert r["shared_lineage_event_fraction"] == 1
    assert r["cross_community_content_lineages_observed"] == 0
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 0


def test_missing_metadata_produces_identification_bounds():
    obs = [event(0, community="a", content=("root",), variant="v1"),
           event(1, community="b", content=("root",)),
           event(2)]
    r = analyse_memetic_observations(obs)["social_resonance"]
    assert r["content_ancestry_coverage_fraction"] == 2 / 3
    assert r["semantic_variant_ratio_lower_bound"] == 1 / 3
    assert r["semantic_variant_ratio_upper_bound"] == 1
    assert r["community_breadth_lower_bound"] == 2
    assert r["community_breadth_upper_bound"] == 3
    assert r["cross_community_lineage_overlap_event_fraction_lower_bound"] == 2 / 3
    assert r["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1
    assert r["cross_community_lineage_overlap_status"] == "PARTIAL"


def test_randomised_bounds_and_non_admission():
    rng = Random(1821)
    for trial in range(150):
        obs = [event(i, community=rng.choice(("a", "b", None)),
                     content=rng.choice(((), ("r",), ("s",))),
                     variant=rng.choice(("x", "y", None)))
               for i in range(rng.randrange(1, 15))]
        g1 = analyse_memetic_observations(obs)
        r = g1["social_resonance"]
        for low, high in (
            ("shared_lineage_event_fraction_lower_bound", "shared_lineage_event_fraction_upper_bound"),
            ("semantic_variant_ratio_lower_bound", "semantic_variant_ratio_upper_bound"),
            ("cross_community_lineage_overlap_event_fraction_lower_bound", "cross_community_lineage_overlap_event_fraction_upper_bound"),
        ):
            assert 0 <= r[low] <= r[high] <= 1
        assert g1["predictive_input"] is False

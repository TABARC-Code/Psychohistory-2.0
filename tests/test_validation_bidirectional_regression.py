from datetime import UTC, datetime
from types import SimpleNamespace

from psychohistory.core.bidirectional import DirectedHypothesis, reciprocal_view
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


def observation(name, ancestry, propagation=False):
    now = datetime(2026, 1, 1, tzinfo=UTC)
    return SimpleNamespace(
        observation_id=name, available_at=now, effective_at=now,
        value=1.0, quality=1.0, revision_type="none", is_propagation=propagation,
        ancestry=tuple(ancestry), content_ancestry=tuple(ancestry),
        carrier=None, actor_id=None, community_id=None, semantic_variant=None,
    )


def test_overlapping_ancestors_form_one_component():
    obs = [observation(str(i), ("shared-a", "shared-b")) for i in range(5)]
    result = validate_observations(obs, datetime(2026, 1, 2, tzinfo=UTC))
    assert result["measurement_informational_breadth_upper_bound"] == 1


def test_separate_ancestry_groups():
    obs = [observation("a", ("x",)), observation("b", ("x",)),
           observation("c", ("y",)), observation("d", ("y",))]
    result = validate_observations(obs, datetime(2026, 1, 2, tzinfo=UTC))
    assert result["measurement_informational_breadth_upper_bound"] == 2


def test_memetic_lineage_fraction_is_bounded():
    obs = [observation(str(i), ("x", "y"), True) for i in range(5)]
    result = analyse_memetic_observations(obs)["social_resonance"]
    assert result["shared_lineage_event_fraction"] == 1.0
    assert result["endogenous_reproduction_fraction"] is None


def test_reverse_edge_not_inferred():
    forward = DirectedHypothesis("economy", "politics", 30)
    view = reciprocal_view([forward])
    assert not view[0]["reverse_present"]
    backward = DirectedHypothesis("politics", "economy", 14)
    view = reciprocal_view([forward, backward])
    assert all(item["reverse_present"] for item in view)
    assert not any(item["admitted"] for item in view)


def test_nonfinite_and_boolean_observations_fail_measurement_validation():
    for invalid in (float("nan"), float("inf"), -float("inf"), True):
        row = observation("bad", ("source",))
        row.value = invalid
        result = validate_observations([row], datetime(2026, 1, 2, tzinfo=UTC))
        assert not result["valid"]
        assert any("invalid numeric value" in e for e in result["errors"])

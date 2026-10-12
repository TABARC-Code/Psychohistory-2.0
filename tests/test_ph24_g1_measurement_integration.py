"""Conservative G1 lineage, numeric-ingestion and Hawkes regression checks."""
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
import math

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations
from psychohistory.g1.hawkes import fit_exponential_hawkes


def event(i, *, content=("root",), variant="v", community="A", ancestry=("collector",)):
    t = datetime(2026, 1, 1, tzinfo=UTC) + timedelta(minutes=i)
    return SimpleNamespace(
        observation_id=f"m{i}", is_propagation=True, effective_at=t, available_at=t,
        quality=1.0, value=1.0, revision_type="none",
        content_ancestry=content, ancestry=ancestry, carrier="social",
        actor_id=f"actor{i}", community_id=community, semantic_variant=variant,
    )


def test_complete_lineage_compatibility():
    events = [event(i, community="A" if i % 2 else "B") for i in range(5)]
    validation = validate_observations(events, datetime(2026, 1, 2, tzinfo=UTC))
    resonance = analyse_memetic_observations(events)["social_resonance"]
    assert validation["content_origin_breadth_upper_bound"] == 1
    assert resonance["shared_lineage_event_fraction"] == 1
    assert resonance["cross_community_lineage_event_fraction"] == 1
    assert resonance["semantic_variant_ratio"] == 1 / 5
    assert analyse_memetic_observations(events)["predictive_input"] is False


def test_missing_lineage_is_not_independent_content():
    events = [event(0, content=()), event(1, content=())]
    result = validate_observations(events, datetime(2026, 1, 2, tzinfo=UTC))
    resonance = analyse_memetic_observations(events)["social_resonance"]
    assert result["content_origin_breadth_upper_bound"] is None
    assert resonance["shared_lineage_event_fraction"] is None
    assert resonance["content_lineage_coverage"] == 0
    assert resonance["cross_community_lineage_event_fraction"] is None


def test_missing_variants_have_bounded_richness():
    events = [event(0, variant="v"), event(1, variant=None)]
    resonance = analyse_memetic_observations(events)["social_resonance"]
    assert resonance["semantic_variant_ratio"] is None
    assert resonance["semantic_variant_observed_lower_bound"] == 0.5
    assert resonance["semantic_variant_possible_upper_bound"] == 1.0


@pytest.mark.parametrize("field,value", [
    ("quality", math.nan), ("quality", math.inf), ("quality", True),
    ("value", math.nan), ("value", math.inf), ("value", True),
])
def test_nonfinite_or_boolean_evidence_rejected(field, value):
    t = datetime(2026, 1, 1, tzinfo=UTC)
    observation = Observation("x", "technology", t, t, 1.0, "source")
    from dataclasses import replace
    observation = replace(observation, **{field: value})
    store = Store(":memory:")
    with pytest.raises(ValueError):
        store.add_observation(observation)
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


def test_naive_timestamp_rejected():
    t = datetime(2026, 1, 1, tzinfo=UTC)
    observation = Observation("x", "health", t, datetime(2026, 1, 1), 1.0, "source")
    with pytest.raises(ValueError):
        Store(":memory:").add_observation(observation)


def test_hawkes_tied_events_not_admitted():
    result = fit_exponential_hawkes([0.1, 0.2, 0.2, 0.3, 0.4], 1.0)
    assert result["status"] == "UNRESOLVED"
    assert "simultaneous" in result["reason"]


def test_cross_community_overlap_is_not_predictive_admission():
    events = [event(i, community="A" if i % 2 else "B") for i in range(6)]
    result = analyse_memetic_observations(events)
    assert result["social_resonance"]["cross_community_lineage_event_fraction"] == 1
    assert result["predictive_input"] is False

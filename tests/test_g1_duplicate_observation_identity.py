"""Direct G1 must not count the same observation twice as independent propagation."""

from datetime import UTC, datetime

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 25, tzinfo=UTC)


def propagation(identifier, community):
    return Observation(
        observation_id=identifier,
        series="g1:narrative",
        effective_at=NOW,
        available_at=NOW,
        value=1.0,
        source="independent-observation",
        evidence_role="propagation",
        ancestry=("measurement-collector",),
        content_ancestry=("narrative-origin",),
        community_id=community,
    )


def test_duplicate_id_cannot_invent_cross_community_spread():
    # One observation repeated with a different community label is not
    # evidence that its narrative reached two communities.
    events = [
        propagation("one-event", "community-a"),
        propagation("one-event", "community-b"),
    ]
    assert validate_observations(events, NOW)["valid"] is False
    result = analyse_memetic_observations(events)
    assert result["status"] == "UNRESOLVED"
    assert "duplicate" in result["reason"]
    assert result["predictive_input"] is False


def test_exact_duplicate_event_is_not_counted_twice():
    event = propagation("one-event", "community-a")
    result = analyse_memetic_observations([event, event])
    assert result["status"] == "UNRESOLVED"
    assert "duplicate" in result["reason"]
    assert result["predictive_input"] is False


def test_distinct_event_ids_retain_bounded_lineage_measurements():
    events = [
        propagation("first-event", "community-a"),
        propagation("second-event", "community-b"),
    ]
    result = analyse_memetic_observations(events)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["propagation"]["events"] == 2
    assert (result["social_resonance"]
            ["cross_community_lineage_overlap_event_fraction_lower_bound"]) == 1.0
    assert result["predictive_input"] is False

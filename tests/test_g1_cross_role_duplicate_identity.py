"""G1 direct analysis must respect observation identities across evidence roles."""

from dataclasses import replace
from datetime import UTC, datetime

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 26, tzinfo=UTC)


def _observation(identifier, role):
    return Observation(
        observation_id=identifier,
        series="g1:narrative" if role == "propagation" else "industrial:shock",
        effective_at=NOW,
        available_at=NOW,
        value=1.0,
        source="independent-collector",
        ancestry=("collector",),
        evidence_role=role,
        content_ancestry=("narrative-root",) if role == "propagation" else (),
        community_id="community-a" if role == "propagation" else None,
    )


def test_cross_role_duplicate_id_is_not_accepted_by_direct_g1():
    rows = [
        _observation("shared-id", "measurement"),
        _observation("shared-id", "propagation"),
        _observation("second-event", "propagation"),
    ]
    assert validate_observations(rows, NOW)["valid"] is False
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert "duplicate" in result["reason"]
    assert result["predictive_input"] is False


def test_duplicate_measurement_identity_invalidates_mixed_direct_sample():
    measurement = _observation("shock-id", "measurement")
    rows = [
        measurement,
        replace(measurement, series="economic:shock"),
        _observation("first-event", "propagation"),
    ]
    assert validate_observations(rows, NOW)["valid"] is False
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert "duplicate" in result["reason"]
    assert result["predictive_input"] is False


def test_distinct_cross_role_identities_preserve_g1_diagnostics():
    rows = [
        _observation("shock-id", "measurement"),
        _observation("first-event", "propagation"),
        replace(_observation("second-event", "propagation"),
                community_id="community-b"),
    ]
    assert validate_observations(rows, NOW)["valid"] is True
    result = analyse_memetic_observations(rows)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["propagation"]["events"] == 2
    assert result["social_resonance"][
        "cross_community_lineage_overlap_event_fraction_lower_bound"
    ] == 1.0
    assert result["predictive_input"] is False


def test_unhashable_measurement_identifier_does_not_crash_direct_g1():
    rows = [
        replace(_observation("shock-id", "measurement"),
                observation_id=["invalid", "id"]),
        _observation("first-event", "propagation"),
    ]
    assert validate_observations(rows, NOW)["valid"] is False
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert "identifier" in result["reason"]
    assert result["predictive_input"] is False

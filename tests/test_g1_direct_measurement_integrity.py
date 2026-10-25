"""Direct G1 measurements must meet the same numeric and clock contract as storage."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 25, 12, tzinfo=UTC)


def event(identifier, **changes):
    fields = {
        "observation_id": identifier,
        "series": "g1:narrative",
        "effective_at": NOW,
        "available_at": NOW,
        "value": 1.0,
        "quality": 1.0,
        "source": "observed",
        "evidence_role": "propagation",
        "ancestry": ("collector",),
        "content_ancestry": ("origin",),
        "community_id": identifier,
    }
    fields.update(changes)
    return Observation(**fields)


@pytest.mark.parametrize("bad", [
    True, "1", None, float("nan"), float("inf"), 2**53 + 1, 1 + 2j,
])
def test_direct_g1_rejects_invalid_original_numeric_value(bad):
    observations = [event("a"), event("b", value=bad)]
    assert validate_observations(observations, NOW)["valid"] is False
    result = analyse_memetic_observations(observations)
    assert result["status"] == "UNRESOLVED"
    assert "numeric" in result["reason"]
    assert result["predictive_input"] is False


@pytest.mark.parametrize("bad", [
    -0.01, 1.01, True, "0.5", float("nan"), float("inf"),
])
def test_direct_g1_rejects_invalid_quality(bad):
    observations = [event("a"), event("b", quality=bad)]
    assert validate_observations(observations, NOW)["valid"] is False
    result = analyse_memetic_observations(observations)
    assert result["status"] == "UNRESOLVED"
    assert "numeric" in result["reason"]
    assert result["predictive_input"] is False


@pytest.mark.parametrize("bad", [
    datetime(2026, 10, 25, 12),
    "2026-10-25T12:00:00Z",
    None,
])
def test_direct_g1_rejects_unverifiable_availability_clock(bad):
    observations = [event("a"), event("b", available_at=bad)]
    assert validate_observations(observations, NOW)["valid"] is False
    result = analyse_memetic_observations(observations)
    assert result["status"] == "UNRESOLVED"
    assert "availability" in result["reason"]
    assert result["predictive_input"] is False


def test_valid_utc_offset_clocks_and_numeric_boundary_preserve_lineage_bounds():
    offset = timezone(timedelta(hours=5, minutes=30))
    rows = [
        event("a", value=0.0, quality=0.0),
        event("b", value=-1.0, quality=1.0,
              effective_at=NOW.astimezone(offset),
              available_at=NOW.astimezone(offset)),
    ]
    assert validate_observations(rows, NOW)["valid"] is True
    result = analyse_memetic_observations(rows)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["social_resonance"]["shared_lineage_event_fraction_lower_bound"] == 1.0
    assert (result["social_resonance"]
            ["cross_community_lineage_overlap_event_fraction_lower_bound"]) == 1.0
    assert result["predictive_input"] is False

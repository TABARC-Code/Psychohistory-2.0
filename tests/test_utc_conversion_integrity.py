"""Reject timezone objects that cannot supply a valid UTC instant."""

from datetime import UTC, datetime, timedelta, timezone, tzinfo

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations
from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 24, 6, 0, tzinfo=UTC)


class BrokenOffset(tzinfo):
    def utcoffset(self, dt):
        raise ValueError("offset provider failed")

    def dst(self, dt):
        return None


class ObservationsOnlyStore:
    def __init__(self, observations):
        self.observations = observations

    def observations_as_of(self, as_of):
        return self.observations


def propagation(name, *, effective_at=NOW, available_at=NOW):
    return Observation(
        name, "g1:meme", effective_at, available_at, 1.0, "collector",
        ancestry=("measurement-record",), evidence_role="propagation",
        content_ancestry=("content-root",), carrier="social",
        actor_id=name, community_id="community", semantic_variant="variant",
    )


@pytest.mark.parametrize("bad", [
    datetime(2026, 10, 24, 6, 0, tzinfo=BrokenOffset()),
    datetime.min.replace(tzinfo=timezone(timedelta(hours=1))),
])
def test_unconvertible_effective_clock_fails_measurement_not_pipeline(bad):
    result = evaluate(
        ObservationsOnlyStore([propagation("valid"), propagation("bad", effective_at=bad)]),
        NOW,
    )
    assert result["g1_measurement"]["valid"] is False
    assert any("invalid effective timestamp" in error
               for error in result["g1_measurement"]["errors"])
    assert result["g1_memetics"]["status"] == "UNRESOLVED"
    assert result["g1_memetics"]["predictive_input"] is False


@pytest.mark.parametrize("bad", [
    datetime(2026, 10, 24, 6, 0, tzinfo=BrokenOffset()),
    datetime.min.replace(tzinfo=timezone(timedelta(hours=1))),
])
def test_unconvertible_availability_clock_fails_measurement(bad):
    result = validate_observations([propagation("bad", available_at=bad)], NOW)
    assert result["valid"] is False
    assert any("invalid availability timestamp" in error for error in result["errors"])


@pytest.mark.parametrize("bad", [
    datetime(2026, 10, 24, 6, 0, tzinfo=BrokenOffset()),
    datetime.min.replace(tzinfo=timezone(timedelta(hours=1))),
])
def test_unconvertible_analysis_cutoff_raises_controlled_value_error(bad):
    with pytest.raises(ValueError, match="timezone-aware"):
        evaluate(ObservationsOnlyStore([]), bad)


def test_valid_offset_conversion_remains_supported():
    offset = timezone(timedelta(hours=5))
    equivalent = NOW.astimezone(offset)
    result = evaluate(ObservationsOnlyStore([propagation("valid", effective_at=equivalent,
                                                        available_at=equivalent)]), NOW)
    assert result["g1_measurement"]["valid"] is True
    assert result["g1_memetics"]["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["g1_memetics"]["predictive_input"] is False

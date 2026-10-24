"""G1 measurement validity must cover visible candidates before event-time filtering."""

from datetime import UTC, datetime, timedelta, tzinfo

import pytest

from psychohistory.core.models import Observation
from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 24, 5, 0, tzinfo=UTC)


class UndefinedOffset(tzinfo):
    def utcoffset(self, dt):
        return None

    def dst(self, dt):
        return None


class ObservationsOnlyStore:
    def __init__(self, observations):
        self.observations = observations

    def observations_as_of(self, as_of):
        return self.observations


def propagation(name, *, effective_at=NOW, available_at=NOW):
    return Observation(
        name, "g1:meme", effective_at, available_at, 1.0, "source",
        ancestry=("collector",), evidence_role="propagation",
        content_ancestry=("root",), carrier="social",
        actor_id=name, community_id="community", semantic_variant="variant",
    )


@pytest.mark.parametrize("bad_effective", [
    datetime(2026, 10, 24, 5, 0),
    datetime(2026, 10, 24, 5, 0, tzinfo=UndefinedOffset()),
    "2026-10-24T05:00:00Z",
])
def test_invalid_effective_clock_cannot_disappear_before_g1_validation(bad_effective):
    result = evaluate(
        ObservationsOnlyStore([
            propagation("valid"),
            propagation("invalid", effective_at=bad_effective),
        ]), NOW,
    )
    assert result["g1_measurement"]["valid"] is False
    assert any("invalid effective timestamp" in error
               for error in result["g1_measurement"]["errors"])
    assert result["g1_memetics"]["status"] == "UNRESOLVED"
    assert result["g1_memetics"]["predictive_input"] is False


def test_invalid_availability_on_future_effective_event_blocks_g1():
    result = evaluate(
        ObservationsOnlyStore([
            propagation("valid"),
            propagation(
                "invalid", effective_at=NOW + timedelta(days=1),
                available_at=datetime(2026, 10, 24, 5, 0),
            ),
        ]), NOW,
    )
    assert result["g1_measurement"]["valid"] is False
    assert result["g1_memetics"]["status"] == "UNRESOLVED"


def test_valid_future_effective_event_is_excluded_without_blocking_current_g1():
    result = evaluate(
        ObservationsOnlyStore([
            propagation("valid"),
            propagation("future", effective_at=NOW + timedelta(days=1)),
        ]), NOW,
    )
    assert result["g1_measurement"]["valid"] is True
    assert result["g1_excluded_future_or_unverifiable_effective_at"] == 1
    assert result["g1_measurement"]["propagation_event_count"] == 1
    assert result["g1_memetics"]["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["g1_memetics"]["predictive_input"] is False

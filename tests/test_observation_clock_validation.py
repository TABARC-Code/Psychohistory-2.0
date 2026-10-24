"""Observation clock validation must fail closed without losing provenance."""

from datetime import UTC, datetime, timedelta, timezone, tzinfo

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations


NOW = datetime(2026, 10, 24, 4, 0, tzinfo=UTC)


class UndefinedOffset(tzinfo):
    def utcoffset(self, dt):
        return None

    def dst(self, dt):
        return None


def observation(*, effective_at=NOW, available_at=NOW):
    return Observation(
        "event", "industrial_supply", effective_at, available_at,
        1.0, "independent-release", ancestry=("source-record",),
    )


@pytest.mark.parametrize("available", [
    datetime(2026, 10, 24, 4, 0),
    datetime(2026, 10, 24, 4, 0, tzinfo=UndefinedOffset()),
    "2026-10-24T04:00:00Z",
])
def test_invalid_availability_clock_is_measurement_error(available):
    result = validate_observations([observation(available_at=available)], NOW)
    assert result["valid"] is False
    assert any("availability timestamp" in error for error in result["errors"])


@pytest.mark.parametrize("effective", [
    datetime(2026, 10, 24, 4, 0),
    datetime(2026, 10, 24, 4, 0, tzinfo=UndefinedOffset()),
    "2026-10-24T04:00:00Z",
])
def test_invalid_effective_clock_is_measurement_error(effective):
    result = validate_observations([observation(effective_at=effective)], NOW)
    assert result["valid"] is False
    assert any("effective timestamp" in error for error in result["errors"])


@pytest.mark.parametrize("cutoff", [
    datetime(2026, 10, 24, 4, 0),
    datetime(2026, 10, 24, 4, 0, tzinfo=UndefinedOffset()),
])
def test_invalid_cutoff_is_rejected(cutoff):
    with pytest.raises(ValueError, match="timezone-aware"):
        validate_observations([observation()], cutoff)


def test_valid_offset_equivalence_and_future_detection():
    same = NOW.astimezone(timezone(timedelta(hours=5)))
    valid = validate_observations([observation(available_at=same)], NOW)
    assert valid["valid"] is True
    future = validate_observations([
        observation(available_at=same + timedelta(microseconds=1))
    ], NOW)
    assert future["valid"] is False
    assert any("future leakage" in error for error in future["errors"])

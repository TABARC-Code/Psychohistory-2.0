"""UTC-convertible visibility boundary for the observation model."""

from datetime import UTC, datetime, timedelta, timezone, tzinfo

import pytest

from psychohistory.core.models import Observation


def _observation(available_at):
    return Observation(
        "visibility-1", "g1:propagation",
        datetime(2026, 10, 24, tzinfo=UTC), available_at,
        1.0, "independent-source", evidence_role="propagation",
    )


@pytest.mark.parametrize(
    "bad_clock",
    [
        datetime(1, 1, 1, tzinfo=timezone(timedelta(hours=1))),
        datetime(9999, 12, 31, 23, 59, 59,
                 tzinfo=timezone(timedelta(hours=-1))),
        datetime(2026, 10, 24),
    ],
)
def test_visibility_rejects_invalid_availability_instead_of_crashing(bad_clock):
    with pytest.raises(ValueError, match="UTC-convertible"):
        _observation(bad_clock).visible(datetime(2026, 10, 24, tzinfo=UTC))


def test_visibility_rejects_invalid_cutoff_instead_of_crashing():
    valid = _observation(datetime(2026, 10, 24, tzinfo=UTC))
    with pytest.raises(ValueError, match="UTC-convertible"):
        valid.visible(datetime(1, 1, 1, tzinfo=timezone(timedelta(hours=1))))


class _BrokenTimezone(tzinfo):
    def utcoffset(self, dt):
        raise ValueError("offset unavailable")

    def dst(self, dt):
        return timedelta(0)


def test_visibility_rejects_failing_timezone_provider():
    with pytest.raises(ValueError, match="UTC-convertible"):
        _observation(datetime(2026, 10, 24, tzinfo=_BrokenTimezone())).visible(
            datetime(2026, 10, 24, tzinfo=UTC)
        )


def test_visibility_preserves_exact_microsecond_and_offset_ordering():
    available = datetime(2026, 10, 24, 15, 0, 0, 1,
                         tzinfo=timezone(timedelta(hours=1)))
    observation = _observation(available)
    assert not observation.visible(datetime(2026, 10, 24, 14, 0, tzinfo=UTC))
    assert observation.visible(datetime(2026, 10, 24, 14, 0, 0, 1, tzinfo=UTC))
    assert observation.visible(datetime(2026, 10, 24, 14, 0, 0, 2, tzinfo=UTC))

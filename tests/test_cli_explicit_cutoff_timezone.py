"""Point-in-time CLI cutoffs must name their timezone explicitly.

A naive wall clock is not a UTC instant. Assigning UTC without evidence can
move the information cutoff and admit observations unavailable at the intended
instant. Explicit UTC and offset clocks remain valid.
"""

from datetime import UTC, datetime

import pytest

from psychohistory.cli import dt


@pytest.mark.parametrize("cutoff", [
    "2026-10-26T19:30:00",
    "2026-10-26T19:30:00.123456",
    "2026-10-26",
])
def test_naive_cli_cutoff_is_not_silently_assigned_utc(cutoff):
    with pytest.raises(ValueError, match="timezone|offset"):
        dt(cutoff)


def test_explicit_offset_preserves_actual_utc_instant():
    parsed = dt("2026-10-26T19:30:00+01:00")
    assert parsed.astimezone(UTC) == datetime(2026, 10, 26, 18, 30, tzinfo=UTC)


def test_explicit_utc_z_suffix_remains_supported():
    assert dt("2026-10-26T18:30:00Z") == datetime(2026, 10, 26, 18, 30, tzinfo=UTC)

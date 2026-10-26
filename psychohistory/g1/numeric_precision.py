"""Shared binary64 checks for G1 event-time estimators."""

import numpy as np

from ..core.numeric_precision import exact_binary64_real


def unit_window_gaps_preserved(events, normalised, window, *, past=(), normalised_past=()):
    """Check that time scaling retains excitation and censoring intervals.

    Preserving strictly ordered timestamps is insufficient: subtracting
    rounded unit times can materially change an adjacent event gap or
    the remaining interval before right censoring. The fitting likelihood
    must reject such data rather than optimise a different event history.
    """
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        physical_remaining = (window - events) / window
        unit_remaining = 1.0 - normalised
        physical_gaps = np.diff(events) / window
        unit_gaps = np.diff(normalised)
        physical_past_gaps = np.diff(past) / window
        unit_past_gaps = np.diff(normalised_past)
    return bool(
        np.allclose(physical_remaining, unit_remaining, rtol=1e-12, atol=0)
        and np.allclose(physical_gaps, unit_gaps, rtol=1e-12, atol=0)
        and np.allclose(physical_past_gaps, unit_past_gaps, rtol=1e-12, atol=0)
    )


__all__ = ["exact_binary64_real", "unit_window_gaps_preserved"]

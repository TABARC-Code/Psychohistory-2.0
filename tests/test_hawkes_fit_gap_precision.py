"""Guard fitted Hawkes diagnostics against lossy unit-window time gaps.

Distinct binary64 timestamps are not enough: dividing by the window can
preserve event order while changing a censoring or excitation interval.
These are numerical integrity tests, not transmission or forecast tests.
"""

from math import nextafter

import numpy as np
import pytest

import psychohistory.g1.hawkes as legacy
from psychohistory.g1.hawkes_prehistory import _prepared


WINDOW = 1e300


def test_observed_history_fit_rejects_distorted_excitation_gap():
    events = [0.0, WINDOW / 10, WINDOW / 4, WINDOW / 2,
              nextafter(WINDOW / 2, float("inf"))]
    physical_gap = (events[-1] - events[-2]) / WINDOW
    unit_gap = events[-1] / WINDOW - events[-2] / WINDOW
    assert physical_gap > 0 and unit_gap > 0
    assert abs(unit_gap / physical_gap - 1) > 0.4
    with pytest.raises(ValueError, match="precision"):
        _prepared(events, [], WINDOW)


def test_observed_history_fit_rejects_distorted_censoring_gap():
    events = [0.0, WINDOW / 10, WINDOW / 4, WINDOW / 2,
              nextafter(WINDOW, 0.0)]
    physical_remaining = (WINDOW - events[-1]) / WINDOW
    unit_remaining = 1.0 - events[-1] / WINDOW
    assert physical_remaining > 0 and unit_remaining > 0
    assert abs(unit_remaining / physical_remaining - 1) > 0.2
    with pytest.raises(ValueError, match="precision"):
        _prepared(events, [], WINDOW)


def test_zero_history_fit_refuses_lossy_gaps_before_optimisation(monkeypatch):
    events = [0.0, WINDOW / 10, WINDOW / 4, WINDOW / 2,
              nextafter(WINDOW / 2, float("inf"))]

    def must_not_fit(*args, **kwargs):
        raise AssertionError("lossy timestamps reached the optimiser")

    monkeypatch.setattr(legacy, "minimize", must_not_fit)
    result = legacy.fit_exponential_hawkes(events, WINDOW)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False
    assert "precision" in result["reason"]


def test_observed_history_preserves_well_spaced_event_times():
    events = [0.0, WINDOW / 8, WINDOW / 4, WINDOW / 2, WINDOW * 0.75]
    u, p, T = _prepared(events, [-WINDOW / 2], WINDOW)
    assert len(u) == len(events)
    assert len(p) == 1
    assert np.all(np.diff(u) > 0)
    assert T == WINDOW

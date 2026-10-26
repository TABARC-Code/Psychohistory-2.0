"""OU transition likelihood must preserve finite subnormal time increments."""

from math import exp, expm1, isfinite, log, pi
from types import SimpleNamespace

import numpy as np
import pytest

import psychohistory.g2.ou as ou


def _probe(monkeypatch, times, values, parameters):
    scores = []

    def capture(objective, initial, **kwargs):
        scores.append(objective(np.asarray(parameters, dtype=float)))
        return SimpleNamespace(success=False, fun=float("inf"))

    monkeypatch.setattr(ou, "minimize", capture)
    result = ou.fit_ou(times, values)
    assert result["status"] == "UNRESOLVED"
    assert len(scores) == 4
    return scores


def test_subnormal_observed_gap_keeps_positive_ou_variance(monkeypatch):
    # A real 1e-320 time increment is distinguishable from zero in binary64.
    # At a=exp(-15), -expm1(-2*a*dt) rounds to zero, although the exact
    # conditional variance sigma**2 * dt * exprel(-2*a*dt) is positive.
    scores = _probe(
        monkeypatch,
        [0.0, 1e-320, 0.5, 1.0],
        [0.0, 1e-160, 0.5, 0.2],
        [-15.0, 0.0, 0.0],
    )
    assert all(isfinite(score) for score in scores)


def test_ordinary_ou_transition_likelihood_is_unchanged(monkeypatch):
    times = np.asarray([0.0, 0.2, 0.5, 1.0])
    values = np.asarray([0.0, 0.1, 0.5, 0.2])
    a, mu, sigma = 1.2, 0.3, 0.7
    scores = _probe(
        monkeypatch, times, values, [log(a), mu, log(sigma)],
    )
    centred = (values - values[0]) / np.ptp(values)
    gaps = np.diff(times) / (times[-1] - times[0])
    expected = 0.0
    for dt, x0, x1 in zip(gaps, centred[:-1], centred[1:]):
        decay = exp(-a * dt)
        mean = mu + (x0 - mu) * decay
        variance = sigma**2 * (-expm1(-2 * a * dt)) / (2 * a)
        expected += 0.5 * (log(2 * pi * variance) + (x1 - mean)**2 / variance)
    assert all(score == pytest.approx(expected, rel=1e-12, abs=1e-12)
               for score in scores)


def test_subnormal_gap_is_not_a_claim_of_identifiability(monkeypatch):
    # A finite likelihood is necessary, not sufficient, for a valid fit.
    scores = _probe(
        monkeypatch,
        [0.0, 1e-320, 0.5, 1.0],
        [0.0, 1e-160, 0.5, 0.2],
        [-15.0, 0.0, 0.0],
    )
    assert all(isfinite(score) for score in scores)

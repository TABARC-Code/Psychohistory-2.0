"""Fixed-parameter Hawkes likelihood must not overflow finite event intensities."""

import math

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


def test_multiple_nearby_events_keep_finite_log_intensity():
    # The third intensity exceeds binary64, but its logarithm and the
    # integrated excitation are finite. This is scoring, not fitted admission.
    gap = 1e-305
    alpha, beta = 1e308, 1e300
    decay = math.exp(-beta * gap)
    expected = (
        math.log(alpha) + math.log(decay)
        + math.log(alpha) + math.log(decay * (1 + decay))
        - (1.0 + 3 * (alpha / beta))
    )
    score = conditional_hawkes_log_likelihood(
        [0.0, gap, 2 * gap], 1.0, mu=1.0, alpha=alpha, beta=beta,
    )
    assert math.isfinite(score)
    assert score == pytest.approx(expected, abs=2e-4)


def test_observed_prehistory_keeps_finite_log_intensity():
    gap = 1e-305
    alpha, beta = 1e308, 1e300
    h0 = math.exp(-beta * gap) + math.exp(-2 * beta * gap)
    expected = math.log(alpha) + math.log(h0) - (
        1.0 + (alpha / beta) * (1.0 + h0)
    )
    score = conditional_hawkes_log_likelihood(
        [0.0], 1.0, prehistory=[-2 * gap, -gap],
        mu=1.0, alpha=alpha, beta=beta,
    )
    assert math.isfinite(score)
    assert score == pytest.approx(expected, abs=2e-4)


def test_impossible_first_event_remains_negative_infinity():
    score = conditional_hawkes_log_likelihood(
        [0.0, 1e-305], 1.0, mu=0.0, alpha=1e308, beta=1e300,
    )
    assert score == -math.inf

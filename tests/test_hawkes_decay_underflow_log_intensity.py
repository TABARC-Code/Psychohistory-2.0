"""Hawkes log intensity must retain excitation below exp() underflow.

The compensator can remain finite even when a single decay factor rounds
to zero. That rounded zero must not erase a large excitation contribution
to a subsequent event's log intensity.
"""

import math

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


MU = 1e-100
ALPHA = 1e300
BETA = 1e300
GAP = 8e-298


def test_remote_observed_prehistory_retains_log_excitation():
    # exp(-800) rounds to zero, but alpha * exp(-800) dominates mu.
    expected = math.log(ALPHA) - BETA * GAP - ALPHA / BETA
    score = conditional_hawkes_log_likelihood(
        [0.0], 1.0, prehistory=[-GAP],
        mu=MU, alpha=ALPHA, beta=BETA,
    )
    assert math.isfinite(score)
    assert score == pytest.approx(expected, abs=1e-10)


def test_in_window_decay_underflow_retains_later_event_excitation():
    # Event zero starts at background intensity. The second still feels
    # the first event despite exp(-800) rounding to zero in binary64.
    expected = math.log(MU) + math.log(ALPHA) - BETA * GAP - 2 * ALPHA / BETA
    score = conditional_hawkes_log_likelihood(
        [0.0, GAP], 1.0, mu=MU, alpha=ALPHA, beta=BETA,
    )
    assert math.isfinite(score)
    assert score == pytest.approx(expected, abs=1e-10)


def test_decay_from_window_start_preserves_prehistory_at_first_event():
    # The pre-window event is only one decay unit before time zero, but
    # the delay from zero to the first in-window event underflows.
    past = -1e-300
    expected = (
        math.log(ALPHA) - BETA * (GAP - past)
        - (ALPHA / BETA) * (1 + math.exp(BETA * past))
    )
    score = conditional_hawkes_log_likelihood(
        [GAP], 1.0, prehistory=[past],
        mu=MU, alpha=ALPHA, beta=BETA,
    )
    assert math.isfinite(score)
    assert score == pytest.approx(expected, abs=1e-10)


def test_negligible_remote_excitation_does_not_change_poisson_scale():
    score = conditional_hawkes_log_likelihood(
        [0.0], 1.0, prehistory=[-GAP],
        mu=1.0, alpha=ALPHA, beta=BETA,
    )
    assert score == pytest.approx(-2.0, abs=1e-12)

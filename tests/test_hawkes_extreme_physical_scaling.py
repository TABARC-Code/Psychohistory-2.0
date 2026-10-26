"""Conditional Hawkes likelihood must retain physical scale at extreme windows."""

import math

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


def test_large_window_decay_overflow_keeps_first_event_likelihood():
    # beta*T overflows, but the physical likelihood is finite.
    T, mu, alpha, beta = 1e308, 1e-308, 1e-308, 10.0
    expected = math.log(mu) - mu * T - alpha / beta
    result = conditional_hawkes_log_likelihood(
        [0.0], T, mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(expected, abs=1e-11)


def test_large_window_preserves_prestart_excitation():
    # A pre-window event at -0.1 has nonzero influence at time zero.
    # Multiplying an infinite scaled beta by a tiny scaled history time
    # must not erase the physically finite beta * (-0.1).
    T, mu, alpha, beta = 1e308, 1e-308, 1e-308, 10.0
    h0 = math.exp(-1.0)
    expected = math.log(mu + alpha * h0) - mu * T - (alpha / beta) * (1 + h0)
    result = conditional_hawkes_log_likelihood(
        [0.0], T, prehistory=[-0.1], mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(expected, abs=1e-11)


def test_large_excitation_and_decay_have_finite_integrated_kernel():
    T, mu, alpha, beta = 1e308, 1e-308, 1e308, 1e308
    expected = math.log(mu) - mu * T - alpha / beta
    result = conditional_hawkes_log_likelihood(
        [0.0], T, mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(expected, abs=1e-11)


def test_tiny_window_does_not_erase_positive_background_intensity():
    T, mu, alpha, beta = 1e-308, 1e-308, 1e-308, 1.0
    result = conditional_hawkes_log_likelihood(
        [0.0], T, mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(math.log(mu), abs=1e-11)


def test_tiny_decay_scale_preserves_prehistory_and_poisson_background():
    T, mu, alpha, beta = 1e-308, 2.0, 1.0, 1e-320
    result = conditional_hawkes_log_likelihood(
        [0.0], T, prehistory=[-T], mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(math.log(3.0), abs=1e-11)


def test_moderate_scale_conditional_likelihood_unchanged():
    T, mu, alpha, beta = 1.0, 2.0, 0.5, 1.5
    h0 = math.exp(-beta * 0.3)
    expected = (
        math.log(mu + alpha * h0)
        - mu * T
        - (alpha / beta) * (1 + h0) * (-math.expm1(-beta * T))
    )
    result = conditional_hawkes_log_likelihood(
        [0.0], T, prehistory=[-0.3], mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(expected, abs=1e-11)

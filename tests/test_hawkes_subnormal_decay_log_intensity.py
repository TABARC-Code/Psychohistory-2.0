"""Subnormal Hawkes decay factors can corrupt finite log intensities.

A subnormal exp(-beta * gap) is not reliably accurate enough to multiply
by a large excitation rate before taking a logarithm.
"""

import math

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


def test_subnormal_prehistory_decay_does_not_distort_log_intensity():
    alpha, beta, mu = 1e300, 1e300, 1e-100
    gap = 7.44e-298
    expected = math.log(alpha) - beta * gap - alpha / beta
    score = conditional_hawkes_log_likelihood(
        [0.0], 1.0, prehistory=[-gap], mu=mu, alpha=alpha, beta=beta,
    )
    assert score == pytest.approx(expected, abs=1e-10)


def test_subnormal_in_window_decay_does_not_distort_log_intensity():
    alpha, beta, mu = 1e300, 1e300, 1e-100
    gap = 7.44e-298
    expected = math.log(mu) + math.log(alpha) - beta * gap - 2 * alpha / beta
    score = conditional_hawkes_log_likelihood(
        [0.0, gap], 1.0, mu=mu, alpha=alpha, beta=beta,
    )
    assert score == pytest.approx(expected, abs=1e-10)

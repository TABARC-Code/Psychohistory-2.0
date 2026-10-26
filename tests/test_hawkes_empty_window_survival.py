"""Empty observed Hawkes windows have exact survival with no excitation history."""

import math

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


@pytest.mark.parametrize(("window", "mu", "alpha", "beta"), [
    (1.0, 2.0, 0.5, 1.0),
    (7.0, 0.25, 4.0, 3.0),
    (1e308, 1e-308, 1e308, 1e308),
    (1e308, 1e-308, 1e-308, 1e308),
    (1.0, 0.0, 1e308, 1e308),
])
def test_empty_window_without_prehistory_has_poisson_survival(
    window, mu, alpha, beta,
):
    # With no events anywhere in the conditioning history, excitation
    # contributes exactly zero regardless of the allowed kernel parameters.
    expected = -mu * window
    result = conditional_hawkes_log_likelihood(
        [], window, prehistory=[], mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(expected, abs=1e-12)


def test_observed_prehistory_still_contributes_to_empty_window_survival():
    mu, alpha, beta = 1.0, 0.7, 1.5
    h0 = math.exp(-0.5 * beta)
    expected = -mu - alpha * h0 * (-math.expm1(-beta)) / beta
    result = conditional_hawkes_log_likelihood(
        [], 1.0, prehistory=[-0.5], mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(expected, abs=1e-12)
    assert result < -mu


def test_nonempty_window_still_integrates_postevent_excitation():
    mu, alpha, beta = 1.0, 0.7, 1.5
    expected = -mu - alpha * (-math.expm1(-0.5 * beta)) / beta
    result = conditional_hawkes_log_likelihood(
        [0.5], 1.0, prehistory=[], mu=mu, alpha=alpha, beta=beta,
    )
    assert result == pytest.approx(expected, abs=1e-12)
    assert result < -mu

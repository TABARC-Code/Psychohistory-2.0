"""Finite-window conditioning, causal chronology and exact compensator tests."""
import numpy as np
import pytest
from scipy.integrate import quad

from psychohistory.g1.hawkes import _log_likelihood_unit_window
from psychohistory.g1.hawkes_prehistory import (
    _log_likelihood_unit_window_observed_history as conditioned,
    conditional_hawkes_log_likelihood, fit_exponential_hawkes_observed_prehistory,
)


def test_empty_prehistory_recovers_legacy_likelihood():
    rng = np.random.default_rng(240143)
    for _ in range(150):
        u = np.sort(rng.uniform(0.001, 0.999, size=12))
        mu, alpha, beta = 2.3, 0.65, 1.4
        assert conditioned(u, np.array([]), mu, alpha, beta) == pytest.approx(
            _log_likelihood_unit_window(u, mu, alpha, beta), abs=2e-12)


def test_observed_history_compensator_against_quadrature():
    u = np.array([0.04, 0.21, 0.7, 0.93])
    p = np.array([-2.0, -0.8, -0.003])
    mu, alpha, beta = 2.0, 0.9, 1.5
    intensity = lambda t: mu + alpha * sum(np.exp(-beta * (t - x))
                                              for x in np.r_[p, u] if x < t)
    integral = sum(quad(intensity, a, b, epsabs=1e-12)[0]
                   for a, b in zip([0.0, *u], [*u, 1.0]))
    expected = sum(np.log(intensity(float(t))) for t in u) - integral
    assert conditioned(u, p, mu, alpha, beta) == pytest.approx(expected, abs=2e-10)


def test_window_unit_rescaling_invariance():
    e, past, T = [0.2, 0.5, 0.9], [-2.0, -0.3], 1.0
    a = conditional_hawkes_log_likelihood(e, T, prehistory=past,
                                          mu=2.0, alpha=0.8, beta=1.5)
    factor = 3600.0
    b = conditional_hawkes_log_likelihood([t * factor for t in e], T * factor,
                                          prehistory=[t * factor for t in past],
                                          mu=2.0/factor, alpha=0.8/factor,
                                          beta=1.5/factor)
    assert b == pytest.approx(a - len(e) * np.log(factor), abs=1e-10)


@pytest.mark.parametrize('bad_past', [[0.0], [0.2], [float('nan')], [-1, -1], [complex(-1, 1)]])
def test_reject_invalid_prehistory(bad_past):
    with pytest.raises(ValueError):
        conditional_hawkes_log_likelihood([0.1], 1.0, prehistory=bad_past,
                                          mu=1.0, alpha=0.5, beta=1.0)


@pytest.mark.parametrize('bad_events', [[-0.1], [1.0], [0.1, 0.1], [complex(0.1, 0.2)]])
def test_reject_invalid_window_events(bad_events):
    with pytest.raises(ValueError):
        conditional_hawkes_log_likelihood(bad_events, 1.0, prehistory=[-0.2],
                                          mu=1.0, alpha=0.5, beta=1.0)


def test_prewindow_fit_retains_identifiability_and_admission_guards():
    e = [0.03, 0.07, 0.13, 0.28, 0.41, 0.55, 0.72, 0.88]
    result = fit_exponential_hawkes_observed_prehistory(e, 1.0, prehistory=[-0.8, -0.2])
    assert result['predictive_input'] is False
    if result['status'] == 'VALID':
        assert result['identifiability_status'] == 'UNVERIFIED'
        assert result['prehistory_event_count'] == 2


def test_zero_event_window_has_exact_survival_likelihood():
    mu, alpha, beta = 0.9, 0.6, 1.5
    past = [-0.8, -0.1]
    h0 = sum(np.exp(beta * p) for p in past)
    expected = -mu - (alpha/beta) * h0 * (-np.expm1(-beta))
    assert conditional_hawkes_log_likelihood([], 1.0, prehistory=past,
                                              mu=mu, alpha=alpha, beta=beta) == pytest.approx(expected)


@pytest.mark.parametrize('bad', [[True], ['0.2'], [2**53 + 1], [-2**53 - 1]])
def test_refuse_lossy_timestamp_domain(bad):
    with pytest.raises(ValueError):
        conditional_hawkes_log_likelihood(bad, 1.0, mu=1.0, alpha=0.5, beta=1.0)


@pytest.mark.parametrize('bad', [True, '1.0', 1+1j])
def test_refuse_invalid_parameter_domain(bad):
    with pytest.raises(ValueError):
        conditional_hawkes_log_likelihood([0.2], 1.0, mu=bad, alpha=0.5, beta=1.0)

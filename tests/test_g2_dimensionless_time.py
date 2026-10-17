"""Synthetic OU dimensional-invariance checks; not empirical forecasting evidence."""
import numpy as np
import pytest
from psychohistory.g2.ou import fit_ou


def series(seed):
    rng = np.random.default_rng(seed)
    x = [0.2]
    decay = np.exp(-0.3 * 0.5)
    for _ in range(159):
        x.append(0.6 + (x[-1] - 0.6) * decay + np.sqrt(
            0.2**2 * (1 - decay**2) / (2 * 0.3)
        ) * rng.normal())
    return np.arange(len(x), dtype=float) * 0.5, x


@pytest.mark.parametrize('seed', [3, 7, 9, 12])
def test_time_unit_invariance(seed):
    times, values = series(seed)
    reference = fit_ou(times, values)
    assert reference['status'] == 'VALID'
    assert reference['boundary_warning'] is False
    for scale in (1e-4, 1e4):
        result = fit_ou(times * scale, values)
        assert result['status'] == 'VALID'
        assert result['boundary_warning'] is False
        assert result['log_likelihood'] == pytest.approx(reference['log_likelihood'], abs=1e-5)
        assert result['mu'] == pytest.approx(reference['mu'], abs=1e-4)
        assert result['a'] * scale == pytest.approx(reference['a'], rel=3e-5)
        assert result['sigma'] * np.sqrt(scale) == pytest.approx(reference['sigma'], rel=3e-5)
        assert result['recovery_time'] / scale == pytest.approx(reference['recovery_time'], rel=3e-5)


def test_unrepresentable_time_spacing_fails_closed():
    assert fit_ou([-1e308, -0.5e308, 0.5e308, 1e308], [0.0, 1.0, 0.5, 0.2])['status'] == 'UNRESOLVED'


def test_invalid_and_constant_inputs():
    assert fit_ou([0, 1, 1, 2], [0, 1, 2, 3])['status'] == 'UNRESOLVED'
    assert fit_ou([0, 1, 2, 3], [1, 1, 1, 1])['status'] == 'UNRESOLVED'


@pytest.mark.parametrize('seed', [2, 11, 19])
def test_irregular_time_unit_invariance(seed):
    rng = np.random.default_rng(seed)
    steps = rng.uniform(0.2, 1.1, size=119)
    times = np.r_[0, np.cumsum(steps)]
    values = [0.1]
    for dt in steps:
        decay = np.exp(-0.25 * dt)
        variance = 0.18**2 * (1 - decay**2) / (2 * 0.25)
        values.append(0.5 + (values[-1] - 0.5) * decay + np.sqrt(variance) * rng.normal())
    reference = fit_ou(times, values)
    assert reference['status'] == 'VALID'
    for scale in (1e-4, 1e4):
        result = fit_ou(times * scale, values)
        assert result['status'] == 'VALID'
        assert result['log_likelihood'] == pytest.approx(reference['log_likelihood'], abs=1e-4)
        assert result['a'] * scale == pytest.approx(reference['a'], rel=5e-4)
        assert result['sigma'] * np.sqrt(scale) == pytest.approx(reference['sigma'], rel=5e-4)

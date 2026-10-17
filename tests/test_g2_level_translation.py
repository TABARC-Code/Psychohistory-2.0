"""OU level-translation invariance: numerical and status regression."""
import numpy as np
from psychohistory.g2.ou import fit_ou

X = np.array([0.2,0.7,0.5,0.8,0.4,0.3,0.6,0.5,0.1,0.4,
              0.3,0.5,0.4,0.6,0.8,0.7,0.5,0.4,0.3,0.2,
              0.4,0.6,0.7,0.5,0.4,0.3,0.5,0.7,0.4,0.2])
T = np.linspace(0,10,len(X))

def test_ou_level_shift_invariance():
    baseline = fit_ou(T, X)
    assert baseline['status'] == 'VALID'
    for shift in (1000, 1e6, 1e9, 1e10):
        candidate = fit_ou(T, X + shift)
        assert candidate['status'] == 'VALID', (shift, candidate)
        assert np.isclose(candidate['a'], baseline['a'], rtol=2e-4), (shift, candidate, baseline)
        assert np.isclose(candidate['sigma'], baseline['sigma'], rtol=2e-4), (shift, candidate, baseline)
        assert np.isclose(candidate['mu'] - shift, baseline['mu'], atol=2e-5), (shift, candidate, baseline)
        assert np.isclose(candidate['log_likelihood'], baseline['log_likelihood'], atol=2e-4), (shift, candidate, baseline)

def test_near_constant_unidentifiable_even_when_shifted():
    for shift in (0, 1e6, 1e10):
        r = fit_ou(T, np.full(len(T), shift + 0.4))
        assert r['status'] == 'UNRESOLVED'

def test_unrepresentable_spread_rejected():
    r = fit_ou([0,1,2,3], [-1e308,1e308,-1e308,1e308])
    assert r['status'] == 'UNRESOLVED'


def test_ou_seeded_translation_stress():
    """Translation must not change OU dynamics on well-resolved histories."""
    for seed in range(40):
        rng = np.random.default_rng(seed)
        t = np.arange(80) * 0.2
        x = np.empty(len(t))
        x[0] = 0.3
        for i in range(1, len(t)):
            d = 0.2
            x[i] = (0.7 + (x[i-1] - 0.7) * np.exp(-1.1 * d)
                    + 0.15 * np.sqrt((1 - np.exp(-2.2 * d)) / 2.2)
                    * rng.normal())
        baseline = fit_ou(t, x)
        assert baseline["status"] == "VALID", (seed, baseline)
        for shift in (1e3, 1e6, 1e9, 1e10, -1e10):
            candidate = fit_ou(t, x + shift)
            assert candidate["status"] == "VALID", (seed, shift, candidate)
            assert np.isclose(candidate["a"], baseline["a"], rtol=2e-4), (seed, shift)
            assert np.isclose(candidate["sigma"], baseline["sigma"], rtol=2e-4), (seed, shift)
            assert np.isclose(candidate["log_likelihood"],
                              baseline["log_likelihood"], rtol=1e-5), (seed, shift)

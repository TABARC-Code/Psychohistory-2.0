import numpy as np
from psychohistory.g2.ou import fit_ou


def test_nonfinite_recovery_time_never_reported_valid():
    rng = np.random.default_rng(5)
    x = np.cumsum(rng.normal(size=40))
    r = fit_ou(np.linspace(0, 1e308, 40), x)
    assert r['status'] == 'UNRESOLVED' or (
        np.isfinite(r['recovery_time']) and r['recovery_time'] > 0
    )

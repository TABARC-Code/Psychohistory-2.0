"""OU observations must remain real through numerical conversion."""

import numpy as np

from psychohistory.g2.ou import fit_ou


_VALUES = np.array([1.0, 0.8, 0.7, 0.55, 0.5, 0.42, 0.4, 0.35])
_TIMES = np.arange(len(_VALUES), dtype=float)


def test_complex_numpy_values_are_not_silently_projected_to_real():
    result = fit_ou(_TIMES, _VALUES.astype(complex) + 1j)
    assert result["status"] == "UNRESOLVED"


def test_complex_numpy_timestamps_are_not_silently_projected_to_real():
    result = fit_ou(_TIMES.astype(complex) + 2j, _VALUES)
    assert result["status"] == "UNRESOLVED"


def test_complex_object_values_are_rejected():
    result = fit_ou(_TIMES, np.array([complex(float(value), 1.0) for value in _VALUES], dtype=object))
    assert result["status"] == "UNRESOLVED"
    assert "complex" in result["reason"]


def test_real_series_remains_eligible_for_fitting():
    result = fit_ou(_TIMES, _VALUES)
    assert result["status"] == "VALID"
    assert result["a"] > 0

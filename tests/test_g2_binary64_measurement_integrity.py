"""Reject lossy G2 OU measurement conversion before estimating transitions."""

import numpy as np
import pytest

from psychohistory.g2.ou import fit_ou


TIMES = np.arange(8, dtype=float)
VALUES = np.array([1.0, 0.8, 0.7, 0.55, 0.5, 0.42, 0.4, 0.35])


def test_extended_precision_time_is_not_silently_rounded():
    times = TIMES.astype(np.longdouble)
    times[3] = np.longdouble("3.000000000000000001")
    if times[3] == float(times[3]):
        pytest.skip("platform longdouble does not distinguish this timestamp")
    result = fit_ou(times, VALUES)
    assert result["status"] == "UNRESOLVED"
    assert "precision" in result["reason"]


def test_extended_precision_value_is_not_silently_rounded():
    values = VALUES.astype(np.longdouble)
    values[2] = np.longdouble("0.7000000000000000001")
    if values[2] == float(values[2]):
        pytest.skip("platform longdouble does not distinguish this value")
    result = fit_ou(TIMES, values)
    assert result["status"] == "UNRESOLVED"
    assert "precision" in result["reason"]


def test_large_integer_time_is_not_silently_rounded():
    times = [0, 1, 2**53 + 1, 2**53 + 5, 2**53 + 7, 2**53 + 9, 2**53 + 11, 2**53 + 13]
    result = fit_ou(times, VALUES)
    assert result["status"] == "UNRESOLVED"
    assert "precision" in result["reason"]


def test_non_numeric_and_boolean_measurements_are_not_accepted():
    for times, values in ((TIMES, [True, *VALUES[1:]]),
                          ([False, *TIMES[1:]], VALUES),
                          (TIMES, ["1.0", *VALUES[1:]])):
        assert fit_ou(times, values)["status"] == "UNRESOLVED"


def test_binary64_exact_inputs_preserve_existing_fit():
    reference = fit_ou(TIMES, VALUES)
    assert reference["status"] == "VALID"
    exact_times = TIMES.astype(np.longdouble)
    exact_values = np.array([1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125], dtype=np.longdouble)
    result = fit_ou(exact_times, exact_values)
    assert result["status"] == "VALID"
    assert np.isfinite(result["log_likelihood"])

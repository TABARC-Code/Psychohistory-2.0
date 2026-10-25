"""Persistence baselines must use the same lossless numeric boundary as observations."""

from fractions import Fraction

import pytest

from psychohistory.prediction.baselines import persistence


@pytest.mark.parametrize("rows", [
    [1.0, 2**53 + 1],
    [2**53 + 1, 1.0],
    [1.0, Fraction(1, 3)],
    [Fraction(1, 3), 1.0],
])
def test_lossy_persistence_inputs_fail_closed(rows):
    result = persistence(rows)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False
    assert "prediction" not in result


def test_exact_rational_persistence_returns_python_float():
    result = persistence([Fraction(1, 4), Fraction(1, 2)])
    assert result["status"] == "VALID"
    assert type(result["prediction"]) is float
    assert result["prediction"] == 0.5
    assert result["validation_scope"] == "ARITHMETIC_ONLY"
    assert result["chronology_status"] == "UNVERIFIED"
    assert result["predictive_input"] is False


def test_exact_numpy_persistence_returns_python_float():
    np = pytest.importorskip("numpy")
    result = persistence([np.int64(3), np.float32(2.5)])
    assert result["status"] == "VALID"
    assert type(result["prediction"]) is float
    assert result["prediction"] == 2.5


def test_extended_precision_measurement_is_not_silently_rounded():
    np = pytest.importorskip("numpy")
    extended = np.longdouble("1.000000000000000001")
    if extended == float(extended):
        pytest.skip("platform longdouble has no additional precision")
    result = persistence([1.0, extended])
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False

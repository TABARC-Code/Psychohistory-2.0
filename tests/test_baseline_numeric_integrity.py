import pytest

from psychohistory.prediction.baselines import base_rate, persistence


@pytest.mark.parametrize("rows", [
    [0, 1, 2], [1, 1, 2], [-1, 1], [0.5, 1], [True, False],
    [float("nan")], [float("inf")], [1+0j], ["0", "1"],
    [0, None], [0, float("-inf")],
])
def test_invalid_binary_outcomes_never_produce_valid_base_rate(rows):
    result = base_rate(rows)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


@pytest.mark.parametrize("rows", [
    [0, float("nan")], [0, float("inf")], [1+2j], [True, 1],
    [1, "2"], [1, None],
])
def test_invalid_persistence_values_are_not_predictions(rows):
    result = persistence(rows)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


def test_valid_base_rate_is_arithmetic_only():
    result = base_rate([0, 1, 1, 0])
    assert result["status"] == "VALID"
    assert result["probability"] == 0.5
    assert result["n"] == 4
    assert result["validation_scope"] == "ARITHMETIC_ONLY"
    assert result["chronology_status"] == "UNVERIFIED"
    assert result["predictive_input"] is False


def test_valid_persistence_is_arithmetic_only():
    result = persistence([1.0, 2.0, 3.5])
    assert result["status"] == "VALID"
    assert result["prediction"] == 3.5
    assert result["chronology_status"] == "UNVERIFIED"
    assert result["predictive_input"] is False


@pytest.mark.parametrize("func", [base_rate, persistence])
def test_empty_series_is_unmeasured(func):
    assert func([])["status"] == "UNMEASURED"


@pytest.mark.parametrize("func", [base_rate, persistence])
def test_invalid_nonsequence_is_unresolved(func):
    assert func(None)["status"] == "UNRESOLVED"


def test_numpy_array_ambiguity_is_handled():
    np = pytest.importorskip("numpy")
    assert base_rate(np.array([0, 1, 1], dtype=int))["status"] == "UNRESOLVED"
    assert persistence(np.array([0.1, 0.2]))["status"] == "VALID"

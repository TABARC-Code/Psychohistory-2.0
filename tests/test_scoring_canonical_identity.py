"""Scoring identity must agree with canonical registration and outcome keys."""
import pytest

from psychohistory.validation.scoring import brier


@pytest.mark.parametrize(
    "identifier", [" forecast-1", "forecast-1 ", " forecast-1 ", "\tforecast-1"]
)
def test_noncanonical_forecast_identity_is_unresolved(identifier):
    result = brier([(identifier, 0.9, 0.5, 1)])
    assert result["status"] == "UNRESOLVED"
    assert result["n"] == 0
    assert "brier" not in result


def test_padded_duplicate_cannot_change_arithmetic_skill():
    rows = [("forecast-1", 0.9, 0.5, 1), (" forecast-1 ", 0.9, 0.5, 1)]
    result = brier(rows)
    assert result["status"] == "UNRESOLVED"
    assert result["n"] == 0
    assert "brier_skill" not in result


def test_canonical_distinct_forecasts_keep_arithmetic_only_scope():
    result = brier([("forecast-1", 0.9, 0.5, 1), ("forecast-2", 0.1, 0.5, 0)])
    assert result["status"] == "MEASURED"
    assert result["n"] == 2
    assert result["brier"] == pytest.approx(0.01)
    assert result["validation_scope"] == "ARITHMETIC_ONLY"
    assert result["predictive_input"] is False

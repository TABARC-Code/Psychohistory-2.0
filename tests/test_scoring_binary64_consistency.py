"""Scoring arithmetic must preserve the exact binary64 evidence boundary.

These are arithmetic-only checks, not matured forecast evaluations.
"""
from fractions import Fraction

import numpy as np
import pytest

from psychohistory.validation.scoring import brier


@pytest.mark.parametrize("row", [
    ("f1", Fraction(1, 3), 0.5, 1),
    ("f1", 0.5, Fraction(2, 3), 1),
])
def test_lossy_fraction_probability_or_baseline_is_unresolved(row):
    result = brier([row])
    assert result["status"] == "UNRESOLVED"
    assert result["n"] == 0
    assert "brier" not in result
    assert "brier_skill" not in result


def test_exact_fraction_inputs_are_scored_as_binary64_floats():
    result = brier([("f1", Fraction(1, 2), Fraction(1, 4), 1)])
    assert result["status"] == "MEASURED"
    assert result["brier"] == pytest.approx(0.25)
    assert type(result["brier"]) is float
    assert result["baseline_brier"] == pytest.approx(0.5625)
    assert type(result["baseline_brier"]) is float
    assert type(result["brier_skill"]) is float
    assert result["predictive_input"] is False


def test_exact_numpy_scalar_inputs_use_binary64_arithmetic():
    result = brier([
        ("f1", np.float32(0.5), np.float32(0.25), 1),
        ("f2", np.float64(0.5), np.float64(0.75), 0),
    ])
    assert result["status"] == "MEASURED"
    assert result["brier"] == pytest.approx(0.25)
    assert type(result["brier"]) is float
    assert type(result["baseline_brier"]) is float
    assert result["validation_scope"] == "ARITHMETIC_ONLY"


def test_exact_fraction_without_baseline_keeps_skill_unmeasured():
    result = brier([("f1", Fraction(1, 2), None, 0)])
    assert result["status"] == "MEASURED"
    assert result["brier"] == pytest.approx(0.25)
    assert type(result["brier"]) is float
    assert "brier_skill" not in result

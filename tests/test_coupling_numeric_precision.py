"""Numerical evidence boundaries for reciprocal lag claims and G23 screening.

Finite is not sufficient: a lossy scalar can change a measured coefficient
or held-out gain before it is compared with registered evidence.
"""
from fractions import Fraction

import pytest

from psychohistory.core.bidirectional import DirectedHypothesis, reciprocal_view
from psychohistory.g23.gate import coupling_gate


@pytest.mark.parametrize("coefficient", [
    2**53 + 1, -(2**53 + 1), Fraction(1, 3),
])
def test_reciprocal_coefficient_rejects_lossy_binary64_values(coefficient):
    with pytest.raises(ValueError, match="coefficient"):
        DirectedHypothesis("industry", "narratives", 7, coefficient=coefficient)


@pytest.mark.parametrize("gain", [2**53 + 1, 10**100])
def test_g23_cannot_mark_lossy_gain_numerically_eligible(gain):
    result = coupling_gate(
        out_of_sample_gain=gain,
        valid_null=True,
        identifiable=True,
        multiplicity_corrected=True,
    )
    assert result["candidate_numerically_eligible"] is False
    assert "no finite positive held-out gain" in result["reasons"]
    assert result["predictive_input"] is False


def test_exact_binary64_coefficients_preserve_unverified_reciprocity():
    forward = DirectedHypothesis(
        "industry", "narratives", 7,
        coefficient=Fraction(1, 2), admitted=True,
        evidence_ids=("physical-report", "narrative-report"),
    )
    reverse = DirectedHypothesis(
        "narratives", "industry", 14, coefficient=-0.25,
    )
    result = reciprocal_view([forward, reverse])
    assert all(row["predictive_input"] is False for row in result)
    assert all(row["admitted"] is False for row in result)
    assert result[0]["reverse_lags"] == [14]


def test_exact_large_gain_remains_diagnostic_only():
    result = coupling_gate(
        out_of_sample_gain=1e300,
        valid_null=True,
        identifiable=True,
        multiplicity_corrected=True,
    )
    assert result["candidate_numerically_eligible"] is True
    assert result["predictive_input"] is False

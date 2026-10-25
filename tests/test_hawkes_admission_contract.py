"""The G1 Hawkes diagnostic must never leave its admission flag undefined.

These are interface-contract regressions, not tests of predictive skill.
"""
import pytest

from psychohistory.g1.hawkes import fit_exponential_hawkes


@pytest.mark.parametrize(
    ("events", "window"),
    [
        ([], 1.0),
        ([0.1], 1.0),
        ([0.1, 0.2, 0.3, 0.4, 0.5], 0.0),
        ([0.1, 0.2, 0.3, 0.4, 1.0], 1.0),
        ([-0.1, 0.2, 0.3, 0.4, 0.5], 1.0),
        ([0.1, 0.1, 0.3, 0.4, 0.5], 1.0),
        ([0.1, 0.2, float("nan"), 0.4, 0.5], 1.0),
        ([0.1, 0.2, 0.3, 0.4, 0.5], float("inf")),
        ([0.1, 0.2, 0.3, 0.4, 0.5], 1e-320),
    ],
)
def test_every_hawkes_result_explicitly_refuses_predictive_admission(events, window):
    result = fit_exponential_hawkes(events, window)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


def test_converged_hawkes_diagnostic_remains_nonadmitted():
    result = fit_exponential_hawkes(
        [0.03, 0.07, 0.13, 0.28, 0.41, 0.55, 0.72, 0.88], 1.0
    )
    assert result["predictive_input"] is False
    if result["status"] == "VALID":
        assert result["identifiability_status"] == "UNVERIFIED"

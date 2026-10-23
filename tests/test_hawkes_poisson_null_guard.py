"""Finite-window Hawkes boundary and Poisson-null identifiability checks."""

import numpy as np
import pytest

from psychohistory.g1.hawkes import fit_exponential_hawkes


def test_right_endpoint_excluded_from_half_open_window():
    result = fit_exponential_hawkes([0.1, 0.3, 0.5, 0.8, 1.0], 1.0)
    assert result["status"] == "UNRESOLVED"
    assert "outside" in result["reason"]


@pytest.mark.parametrize("scale", [1.0, 60.0, 3600.0])
def test_near_poisson_fit_does_not_claim_identifiable_excitation(scale):
    events = np.array([0.1, 0.3, 0.5, 0.8, 0.999]) * scale
    result = fit_exponential_hawkes(events, scale)
    assert result["status"] == "UNRESOLVED"
    assert "unidentifiable" in result["reason"]
    assert result["predictive_input"] is False
    assert 0.0 <= result["branching_ratio_candidate"] < 1.0


def test_clustered_control_remains_eligible_for_non_admitted_diagnostic():
    events = [0.02, 0.03, 0.04, 0.05, 0.06, 0.6, 0.61, 0.62, 0.63, 0.64]
    result = fit_exponential_hawkes(events, 1.0)
    assert result["status"] == "VALID"
    assert result["branching_ratio"] > 0.1
    assert result["predictive_input"] is False
    assert result["identifiability_status"] == "UNVERIFIED"

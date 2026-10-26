"""Reject finite prehistory timestamps lost by window normalisation."""

import math

import pytest

from psychohistory.g1.hawkes_prehistory import (
    conditional_hawkes_log_likelihood,
    fit_exponential_hawkes_observed_prehistory,
)


TINY_WINDOW = 1e-300
IN_WINDOW = [fraction * TINY_WINDOW for fraction in (0.1, 0.2, 0.4, 0.6, 0.8)]


@pytest.mark.parametrize("prehistory", [
    [-1e308],
    [-1e308, -1e307],
])
def test_conditional_likelihood_rejects_prehistory_normalisation_overflow(prehistory):
    # Each source timestamp is finite. Dividing by a very short window
    # overflows to -inf, discarding the observed conditioning history.
    with pytest.raises(ValueError, match="precision"):
        conditional_hawkes_log_likelihood(
            IN_WINDOW, TINY_WINDOW, prehistory=prehistory,
            mu=1e300, alpha=1e300, beta=1e-308,
        )


def test_prehistory_fit_rejects_normalisation_overflow_before_optimising():
    result = fit_exponential_hawkes_observed_prehistory(
        IN_WINDOW, TINY_WINDOW, prehistory=[-1e308, -1e307],
    )
    assert result["status"] == "UNRESOLVED"
    assert "precision" in result["reason"]
    assert result["predictive_input"] is False


def test_finite_normalised_prehistory_remains_usable():
    value = conditional_hawkes_log_likelihood(
        [0.2, 0.5, 0.8], 1.0, prehistory=[-1.5, -0.25],
        mu=2.0, alpha=0.5, beta=1.0,
    )
    assert math.isfinite(value)

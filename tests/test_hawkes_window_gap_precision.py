"""Physical-time gap checks for conditional Hawkes likelihoods.

Unit-window normalisation can preserve distinct event timestamps while
distorting their differences and right-censoring intervals. Compare against
independent physical-time likelihood expressions, not the production scorer.
"""

from math import exp, expm1, log, nextafter

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


def test_censoring_interval_near_window_end_uses_physical_gap():
    window = 1e300
    event = nextafter(window, 0.0)
    mu, alpha, beta = 1e-300, 1e-280, 1e-300
    # Single event has background intensity only. The integrated excitation
    # must use window-event, not window*(1-event/window).
    expected = (
        log(mu) - mu * window
        - (alpha / beta) * (-expm1(-beta * (window - event)))
    )
    actual = conditional_hawkes_log_likelihood(
        [event], window, mu=mu, alpha=alpha, beta=beta
    )
    assert actual == pytest.approx(expected, rel=1e-12, abs=1e-8)


def test_adjacent_event_excitation_uses_physical_gap():
    window = 1e300
    first = window / 2
    second = nextafter(first, float("inf"))
    mu, alpha, beta = 1e-300, 1e-299, 1e-284
    # With two events, the second intensity depends on their exact physical
    # gap. Both timestamps survive normalisation, but subtraction in unit
    # time loses a material fraction of the observed separation.
    expected = (
        log(mu)
        + log(mu + alpha * exp(-beta * (second - first)))
        - mu * window
        - (alpha / beta) * sum(
            -expm1(-beta * (window - event))
            for event in (first, second)
        )
    )
    actual = conditional_hawkes_log_likelihood(
        [first, second], window, mu=mu, alpha=alpha, beta=beta
    )
    assert actual == pytest.approx(expected, rel=1e-12, abs=1e-8)

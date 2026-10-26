"""Physical Hawkes intensities must survive subnormal unit-rate scaling."""

from math import exp, expm1, log

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


WINDOW = 1e-300
MU = 1e-20
ALPHA = 1e-20
BETA = 1e300
EVENTS = (2e-301, 4e-301, 7e-301)


def _physical_reference(events, prehistory=()):
    # Direct finite-window likelihood in physical units. In particular,
    # neither the background rate nor excitation is first multiplied by T.
    intensity_log = sum(
        log(MU + ALPHA * sum(
            exp(-BETA * (time - prior))
            for prior in (*prehistory, *events) if prior < time
        ))
        for time in events
    )
    integral = MU * WINDOW + (ALPHA / BETA) * (
        sum(-expm1(-BETA * (WINDOW - time)) for time in events)
        + sum(exp(BETA * time) * -expm1(-BETA * WINDOW)
              for time in prehistory)
    )
    return intensity_log - integral


@pytest.mark.parametrize("prehistory", [(), (-1e-301,)])
def test_subnormal_scaled_background_and_excitation_use_physical_likelihood(prehistory):
    # mu*T and alpha*T are subnormal but positive. They retain only a
    # few significant digits, changing a finite log likelihood even though
    # event times, ordering and censoring intervals normalise correctly.
    assert 0 < MU * WINDOW < 2.2250738585072014e-308
    assert 0 < ALPHA * WINDOW < 2.2250738585072014e-308
    score = conditional_hawkes_log_likelihood(
        EVENTS, WINDOW, prehistory=prehistory,
        mu=MU, alpha=ALPHA, beta=BETA,
    )
    assert score == pytest.approx(
        _physical_reference(EVENTS, prehistory), abs=1e-10
    )

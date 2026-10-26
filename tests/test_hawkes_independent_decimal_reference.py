"""Independent finite-window Hawkes reference, including observed prehistory.

Decimal arithmetic checks the exponential kernel directly rather than reusing
production recurrence, logsumexp or unit-window normalisation. These are
numerical regression tests, not tests of endogenous transmission or skill.
"""

from decimal import Decimal, localcontext
from math import isfinite, log

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


def _decimal_reference(events, prehistory, window, mu, alpha, beta):
    with localcontext() as context:
        context.prec = 85
        d = lambda value: Decimal.from_float(float(value))
        times = [d(value) for value in events]
        history = [d(value) for value in prehistory]
        T, background, excitation, decay = map(d, (window, mu, alpha, beta))
        log_events = Decimal(0)
        for event in times:
            intensity = background + excitation * sum(
                ((-decay * (event - previous)).exp()
                 for previous in history + times if previous < event),
                Decimal(0),
            )
            log_events += intensity.ln()
        background_integral = background * T
        past_integral = sum(
            (excitation / decay) * (decay * past).exp()
            * (Decimal(1) - (-decay * T).exp())
            for past in history
        )
        event_integral = sum(
            (excitation / decay) *
            (Decimal(1) - (-decay * (T - event)).exp())
            for event in times
        )
        return float(log_events - background_integral - past_integral - event_integral)


@pytest.mark.parametrize(
    "events,prehistory,T,mu,alpha,beta",
    [
        ([0.0, 8e-298], (), 1.0, 1e-100, 1e300, 1e300),
        ([0.0], [-8e-298], 1.0, 1e-100, 1e300, 1e300),
        ([8e-298], [-1e-300], 1.0, 1e-100, 1e300, 1e300),
        ([0.02, 0.17, 0.63], [-1.1, -0.06], 1.0, 1.7, 0.8, 2.1),
        ([], [-0.5, -0.1], 1.0, 0.9, 0.6, 1.5),
        ([0.01, 0.09, 0.18], [], 0.2, 1.2, 0.7, 1.4),
    ],
)
def test_conditional_hawkes_matches_independent_decimal_reference(
    events, prehistory, T, mu, alpha, beta
):
    expected = _decimal_reference(events, prehistory, T, mu, alpha, beta)
    observed = conditional_hawkes_log_likelihood(
        events, T, prehistory=prehistory, mu=mu, alpha=alpha, beta=beta
    )
    assert isfinite(expected) and isfinite(observed)
    assert observed == pytest.approx(expected, rel=1e-12, abs=2e-10)


def test_hawkes_time_unit_conversion_preserves_physical_density():
    events = [0.02, 0.17, 0.63]
    history = [-1.1, -0.06]
    base = conditional_hawkes_log_likelihood(
        events, 1.0, prehistory=history, mu=1.7, alpha=0.8, beta=2.1
    )
    for factor in (1e-6, 1e-3, 60.0, 3600.0, 1e6):
        rescaled = conditional_hawkes_log_likelihood(
            [factor * t for t in events], factor,
            prehistory=[factor * t for t in history],
            mu=1.7 / factor, alpha=0.8 / factor, beta=2.1 / factor,
        )
        assert rescaled == pytest.approx(
            base - len(events) * log(factor), abs=1e-9
        )

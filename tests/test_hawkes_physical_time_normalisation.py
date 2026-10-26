"""Physical-time Hawkes scoring must not depend on lossy normalisation.

The fitter may refuse collapsed unit-window timestamps. A fixed-parameter
conditional likelihood can instead evaluate exact validated physical times.
"""

from math import expm1, log

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


def test_near_origin_prehistory_does_not_disappear_in_huge_window():
    score = conditional_hawkes_log_likelihood(
        [], 1e308, prehistory=[-1e-308],
        mu=1e-308, alpha=1e-308, beta=1e-308,
    )
    # The prehistory event is real, however small its physical offset.
    expected = -1.0 + expm1(-1.0)
    assert score == pytest.approx(expected, abs=1e-12)


def test_distant_prehistory_does_not_overflow_tiny_window_normalisation():
    score = conditional_hawkes_log_likelihood(
        [], 1e-308, prehistory=[-1e308],
        mu=1e308, alpha=1e308, beta=1e308,
    )
    assert score == pytest.approx(-1.0, abs=1e-12)


def test_positive_event_at_extreme_scale_is_not_rounded_to_window_origin():
    score = conditional_hawkes_log_likelihood(
        [1e-308], 1e308,
        mu=1e-308, alpha=1e-308, beta=1e-308,
    )
    expected = log(1e-308) - 1.0 + expm1(-1.0)
    assert score == pytest.approx(expected, abs=1e-10)


def test_distinct_physical_events_are_not_merged_by_unit_window():
    score = conditional_hawkes_log_likelihood(
        [1e-308, 2e-308], 1e308,
        mu=1e-308, alpha=1e-308, beta=1e-308,
    )
    expected = log(1e-308) + log(2e-308) - 1.0 + 2 * expm1(-1.0)
    assert score == pytest.approx(expected, abs=1e-10)


@pytest.mark.parametrize(
    "events,prehistory",
    [
        ([1.0, 1.0], []),
        ([1.0], [0.0]),
        ([1e308], []),
        ([1.0], [1.0]),
    ],
)
def test_physical_fallback_does_not_relax_invalid_event_windows(events, prehistory):
    with pytest.raises(ValueError):
        conditional_hawkes_log_likelihood(
            events, 1e308, prehistory=prehistory,
            mu=1e-308, alpha=1e-308, beta=1e-308,
        )

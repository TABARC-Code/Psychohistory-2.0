"""A zero-excitation Hawkes model is a Poisson process at every decay scale."""

import math

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


@pytest.mark.parametrize(
    ("events", "window", "prehistory", "mu", "beta", "expected"),
    [
        ([], 1e308, (), 1e-308, 1e308, -(1e-308 * 1e308)),
        ([0.25, 1.5], 2.0, (), 2.0, 1e308, 2 * math.log(2.0) - 4.0),
        ([], 1e-308, (), 1e308, 1e-320, -(1e308 * 1e-308)),
        ([0.25], 2.0, (-0.1, -0.2), 2.0, 1e308, math.log(2.0) - 4.0),
        ([], 2.0, (), 0.0, 1e308, 0.0),
    ],
)
def test_zero_excitation_ignores_unidentifiable_decay_scale(
    events, window, prehistory, mu, beta, expected,
):
    score = conditional_hawkes_log_likelihood(
        events, window, prehistory=prehistory,
        mu=mu, alpha=0.0, beta=beta,
    )
    assert score == pytest.approx(expected, rel=1e-12, abs=1e-12)


def test_zero_background_zero_excitation_cannot_explain_an_event():
    score = conditional_hawkes_log_likelihood(
        [0.25], 2.0, mu=0.0, alpha=0.0, beta=1e308,
    )
    assert score == -math.inf


def test_nonzero_excitation_still_uses_conditional_hawkes_model():
    score = conditional_hawkes_log_likelihood(
        [0.2, 0.5], 1.0, prehistory=[-0.8, -0.1],
        mu=2.0, alpha=1.0, beta=1.0,
    )
    assert math.isfinite(score)

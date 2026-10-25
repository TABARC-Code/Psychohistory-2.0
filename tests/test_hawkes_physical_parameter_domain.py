"""Physical parameter-domain guards for conditional Hawkes diagnostics."""

import math

import pytest

from psychohistory.g1.hawkes_prehistory import conditional_hawkes_log_likelihood


@pytest.mark.parametrize(
    ("mu", "alpha", "beta"),
    [
        (-0.1, 0.5, 1.0),
        (0.5, -0.1, 1.0),
        (0.5, 0.1, 0.0),
        (0.5, 0.1, -1.0),
    ],
)
def test_conditional_likelihood_rejects_invalid_physical_parameters(mu, alpha, beta):
    with pytest.raises(ValueError, match="nonnegative|positive"):
        conditional_hawkes_log_likelihood(
            [0.2, 0.5], 1.0, prehistory=[-0.3],
            mu=mu, alpha=alpha, beta=beta,
        )


def test_valid_poisson_null_still_has_finite_likelihood():
    events = [0.2, 0.5]
    mu = 2.0
    score = conditional_hawkes_log_likelihood(
        events, 1.0, prehistory=[-0.3], mu=mu, alpha=0.0, beta=1.0,
    )
    assert score == pytest.approx(len(events) * math.log(mu) - mu)


def test_empty_event_zero_intensity_has_valid_survival_likelihood():
    score = conditional_hawkes_log_likelihood(
        [], 1.0, mu=0.0, alpha=0.0, beta=1.0,
    )
    assert score == 0.0

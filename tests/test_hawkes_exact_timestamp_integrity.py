"""Reject lossy timestamp conversion before fitting Hawkes event histories."""

import numpy as np
import pytest

from psychohistory.g1.hawkes import fit_exponential_hawkes


CLUSTER = [0.02, 0.03, 0.04, 0.05, 0.06, 0.6, 0.61, 0.62, 0.63, 0.64]
EXTENDED = np.finfo(np.longdouble).eps < np.finfo(np.float64).eps
requires_extended = pytest.mark.skipif(
    not EXTENDED, reason="longdouble is binary64 on this platform"
)


@requires_extended
def test_extended_precision_event_not_silently_rounded():
    changed = np.longdouble("0.020000000000000000001")
    assert changed != float(changed)
    result = fit_exponential_hawkes([changed, *CLUSTER[1:]], 1.0)
    assert result["status"] == "UNRESOLVED"
    assert "precision" in result["reason"]
    assert result["predictive_input"] is False


@requires_extended
def test_extended_precision_window_not_silently_rounded():
    changed = np.longdouble("1.0000000000000000002")
    assert changed != float(changed)
    result = fit_exponential_hawkes(CLUSTER, changed)
    assert result["status"] == "UNRESOLVED"
    assert "precision" in result["reason"]


@requires_extended
def test_in_window_event_must_not_round_to_right_endpoint():
    changed = np.longdouble("0.99999999999999999995")
    assert changed < 1.0 and float(changed) == 1.0
    result = fit_exponential_hawkes([*CLUSTER[:-1], changed], 1.0)
    assert result["status"] == "UNRESOLVED"
    assert "precision" in result["reason"]


@pytest.mark.parametrize("value", [2**53 + 1, -(2**53 + 1)])
def test_integer_beyond_exact_binary64_domain_rejected(value):
    result = fit_exponential_hawkes([*CLUSTER[:-1], value], float(2**55))
    assert result["status"] == "UNRESOLVED"
    assert "precision" in result["reason"]


def test_exact_numpy_float32_inputs_preserved():
    result = fit_exponential_hawkes(
        np.array(CLUSTER, dtype=np.float32), np.float32(1.0)
    )
    assert "precision" not in result.get("reason", "")
    assert result["predictive_input"] is False


def test_ordinary_binary64_cluster_unchanged():
    result = fit_exponential_hawkes(CLUSTER, 1.0)
    assert result["status"] == "VALID"
    assert result["predictive_input"] is False

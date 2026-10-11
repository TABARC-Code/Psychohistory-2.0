import numpy as np
from psychohistory.g1.hawkes import fit_exponential_hawkes
from psychohistory.g2.ou import fit_ou


def test_hawkes_rejects_events_outside_window():
    assert fit_exponential_hawkes([-1, 1, 2, 3, 4], 5)["status"] == "UNRESOLVED"
    assert fit_exponential_hawkes([1, 2, 3, 4, 6], 5)["status"] == "UNRESOLVED"


def test_hawkes_rejects_invalid_window_and_nan():
    assert fit_exponential_hawkes([0, 1, 2, 3, 4], 0)["status"] == "UNRESOLVED"
    assert fit_exponential_hawkes([0, 1, 2, np.nan, 4], 5)["status"] == "UNRESOLVED"


def test_ou_rejects_mismatched_dimensions():
    assert fit_ou([0, 1, 2, 3], [1, 2, 3, 4, 5])["status"] == "UNRESOLVED"


def test_ou_rejects_unordered_times():
    assert fit_ou([0, 2, 1, 3], [1, 2, 3, 4])["status"] == "UNRESOLVED"


def test_ou_rejects_constant_series():
    assert fit_ou([0, 1, 2, 3], [2, 2, 2, 2])["status"] == "UNRESOLVED"


def test_ou_rejects_nonfinite_series():
    assert fit_ou([0, 1, 2, 3], [1, 2, np.inf, 4])["status"] == "UNRESOLVED"

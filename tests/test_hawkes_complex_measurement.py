"""Complex event timestamps must not be silently projected onto the real axis."""
import warnings

import numpy as np

from psychohistory.g1.hawkes import fit_exponential_hawkes


EVENTS = np.array([0.10, 0.11, 0.12, 0.13, 0.40, 0.41, 0.42, 0.80, 0.81, 0.82])


def test_complex_event_array_rejected_without_cast_warning():
    events = EVENTS + 1j * np.arange(1, len(EVENTS) + 1)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = fit_exponential_hawkes(events, 1.0)
    assert result["status"] == "UNRESOLVED"
    assert "complex" in result["reason"]
    assert result["predictive_input"] is False
    assert not caught


def test_complex_event_array_rejected_even_with_zero_imaginary_part():
    result = fit_exponential_hawkes(EVENTS.astype(complex), 1.0)
    assert result["status"] == "UNRESOLVED"
    assert "complex" in result["reason"]


def test_complex_object_array_rejected():
    events = np.array([complex(t, 1) for t in EVENTS], dtype=object)
    result = fit_exponential_hawkes(events, 1.0)
    assert result["status"] == "UNRESOLVED"
    assert "complex" in result["reason"]


def test_complex_numpy_scalar_window_rejected():
    result = fit_exponential_hawkes(EVENTS, np.complex128(1.0 + 2j))
    assert result["status"] == "UNRESOLVED"
    assert "complex" in result["reason"]


def test_real_measurements_remain_eligible_for_non_admitted_diagnostic():
    result = fit_exponential_hawkes(EVENTS, 1.0)
    assert result["status"] == "VALID"
    assert result["identifiability_status"] == "UNVERIFIED"
    assert result["predictive_input"] is False

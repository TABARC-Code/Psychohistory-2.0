"""Reject event-time underflow at the normalised Hawkes window origin."""

from psychohistory.g1.hawkes import fit_exponential_hawkes


def test_nonzero_event_does_not_become_origin_event():
    events = [1e-250, 1e50, 2e50, 3e50, 4e50]
    result = fit_exponential_hawkes(events, 1e100)
    assert result["status"] == "UNRESOLVED"
    assert "origin" in result["reason"]
    assert result["predictive_input"] is False


def test_true_origin_is_not_rejected_as_underflow():
    result = fit_exponential_hawkes([0.0, 1e50, 2e50, 3e50, 4e50], 1e100)
    assert result.get("reason", "") != "event times collapse to window origin at normalised precision"


def test_ordinary_positive_events_not_rejected_as_underflow():
    result = fit_exponential_hawkes([0.1, 0.2, 0.3, 0.4, 0.5], 1.0)
    assert result.get("reason", "") != "event times collapse to window origin at normalised precision"

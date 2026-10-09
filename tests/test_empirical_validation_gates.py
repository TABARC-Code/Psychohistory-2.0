"""Regression tests for point-in-time empirical validation.

Synthetic fixtures only. These tests must not be reported as forecasting skill.
"""
from datetime import datetime
import pytest

from psychohistory.core.models import Forecast, Observation
from psychohistory.core.store import Store


def dt(s):
    return datetime.fromisoformat(s)


def test_observations_use_absolute_time(tmp_path):
    store = Store(tmp_path / "observations.db")
    cut = dt("2026-10-07T00:00:00+00:00")
    for key, available in [
        ("future", "2026-10-06T23:30:00-02:00"),
        ("past", "2026-10-07T01:00:00+02:00"),
    ]:
        store.add_observation(Observation(
            observation_id=key, series="example",
            effective_at=dt("2026-10-01T00:00:00+00:00"),
            available_at=dt(available), value=1.0, source="synthetic"
        ))
    assert [o.observation_id for o in store.observations_as_of(cut)] == ["past"]


@pytest.mark.parametrize("outcome", [0.2, 0.9, 1.2, -0.2, "1", None])
def test_reject_non_binary_outcomes(tmp_path, outcome):
    store = Store(tmp_path / "outcomes.db")
    with pytest.raises((ValueError, TypeError)):
        store.resolve("example", outcome, dt("2026-10-30T00:00:00+00:00"))


@pytest.mark.parametrize("baseline", [-0.1, 1.2, float("nan"), float("inf")])
def test_reject_invalid_baseline(tmp_path, baseline):
    store = Store(tmp_path / "forecast.db")
    with pytest.raises(ValueError):
        store.add_forecast(Forecast("f", "event",
            dt("2026-10-07T00:00:00+00:00"),
            dt("2026-10-29T09:30:00+00:00"), 0.5, "synthetic", baseline))


def test_scoring_cutoff_and_first_release(tmp_path):
    store = Store(tmp_path / "scoring.db")
    store.add_forecast(Forecast("f", "event",
        dt("2026-10-07T00:00:00+00:00"),
        dt("2026-10-29T09:30:00+00:00"), 0.6, "synthetic", 0.5))
    store.resolve("event", 1, dt("2026-10-29T10:00:00+00:00"), "first_release")
    store.resolve("event", 0, dt("2026-11-03T10:00:00+00:00"), "revision")
    assert store.scored(as_of=dt("2026-10-28T00:00:00+00:00")) == []
    assert len(store.scored(as_of=dt("2026-10-30T00:00:00+00:00"))) == 1
    assert len(store.scored(as_of=dt("2026-11-05T00:00:00+00:00"))) == 1

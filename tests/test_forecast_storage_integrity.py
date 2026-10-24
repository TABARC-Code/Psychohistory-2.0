"""Forecast storage must preserve registration arithmetic and UTC chronology.

SQLite accepts some numerical scalars as BLOBs. An unverified local database
is not the immutable forecast ledger and must never grant predictive admission.
"""

from datetime import UTC, datetime, timedelta, timezone

import numpy as np
import pytest

from psychohistory.core.models import Forecast
from psychohistory.core.store import Store


ORIGIN = datetime(2026, 10, 24, 12, tzinfo=UTC)
END = ORIGIN + timedelta(days=2)


def forecast(*, probability=0.4, baseline=0.5, origin=ORIGIN, horizon=END,
             forecast_id="f1", event_id="e1", model="development"):
    return Forecast(forecast_id, event_id, origin, horizon, probability,
                    model, baseline)


@pytest.mark.parametrize("invalid", [
    True, False, float("nan"), float("inf"), -0.01, 1.01, "0.4", None,
])
def test_invalid_probability_rejected_before_storage(tmp_path, invalid):
    store = Store(tmp_path / "forecast.sqlite")
    with pytest.raises(ValueError):
        store.add_forecast(forecast(probability=invalid))
    assert store.db.execute("SELECT COUNT(*) FROM forecasts").fetchone()[0] == 0


@pytest.mark.parametrize("invalid", [
    True, False, float("nan"), float("-inf"), -0.01, 1.01, "0.5",
])
def test_invalid_baseline_rejected_before_storage(tmp_path, invalid):
    store = Store(tmp_path / "forecast.sqlite")
    with pytest.raises(ValueError):
        store.add_forecast(forecast(baseline=invalid))
    assert store.db.execute("SELECT COUNT(*) FROM forecasts").fetchone()[0] == 0


@pytest.mark.parametrize("origin,horizon", [
    (ORIGIN.replace(tzinfo=None), END),
    (ORIGIN, END.replace(tzinfo=None)),
    (ORIGIN, ORIGIN),
    (END, ORIGIN),
    (datetime.min.replace(tzinfo=timezone(timedelta(hours=1))), END),
])
def test_invalid_forecast_window_rejected(tmp_path, origin, horizon):
    store = Store(tmp_path / "forecast.sqlite")
    with pytest.raises(ValueError):
        store.add_forecast(forecast(origin=origin, horizon=horizon))
    assert store.db.execute("SELECT COUNT(*) FROM forecasts").fetchone()[0] == 0


@pytest.mark.parametrize("field", ["forecast_id", "event_id", "model"])
def test_missing_registration_identifiers_rejected(tmp_path, field):
    store = Store(tmp_path / "forecast.sqlite")
    with pytest.raises(ValueError):
        store.add_forecast(forecast(**{field: "  "}))
    assert store.db.execute("SELECT COUNT(*) FROM forecasts").fetchone()[0] == 0


def test_valid_numpy_probabilities_persist_as_sqlite_real(tmp_path):
    store = Store(tmp_path / "forecast.sqlite")
    store.add_forecast(forecast(probability=np.float32(0.5),
                                baseline=np.int64(1)))
    row = store.db.execute(
        "SELECT typeof(probability), probability, "
        "typeof(baseline_probability), baseline_probability FROM forecasts"
    ).fetchone()
    assert row == ("real", 0.5, "real", 1.0)
    assert store.scored() == []


def test_missing_baseline_and_second_offset_clocks_remain_valid(tmp_path):
    store = Store(tmp_path / "forecast.sqlite")
    offset = timezone(timedelta(hours=5, minutes=30, seconds=45))
    store.add_forecast(forecast(baseline=None,
                                origin=ORIGIN.astimezone(offset),
                                horizon=END.astimezone(offset)))
    row = store.db.execute(
        "SELECT origin,horizon_end,baseline_probability FROM forecasts"
    ).fetchone()
    assert datetime.fromisoformat(row[0]).astimezone(UTC) == ORIGIN
    assert datetime.fromisoformat(row[1]).astimezone(UTC) == END
    assert row[2] is None
    assert store.scored() == []

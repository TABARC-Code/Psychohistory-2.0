"""Registration and outcome identities must be canonical before evidence joins.

These tests concern local SQLite integrity, not immutable forecast admission.
"""
from datetime import UTC, datetime, timedelta

import pytest

from psychohistory.core.models import Forecast
from psychohistory.core.store import Store


ORIGIN = datetime(2026, 10, 25, 12, tzinfo=UTC)


@pytest.mark.parametrize("field", ("forecast_id", "event_id", "model"))
def test_padded_forecast_identity_is_rejected(tmp_path, field):
    store = Store(tmp_path / "registration.sqlite")
    values = dict(forecast_id="forecast-1", event_id="industrial-event",
                  origin=ORIGIN, horizon_end=ORIGIN + timedelta(days=2),
                  probability=0.4, model="diagnostic")
    values[field] = " " + values[field] + " "
    with pytest.raises(ValueError):
        store.add_forecast(Forecast(**values))
    assert store.db.execute("SELECT COUNT(*) FROM forecasts").fetchone()[0] == 0


@pytest.mark.parametrize("field", ("event_id", "vintage"))
def test_padded_new_outcome_identity_is_rejected(tmp_path, field):
    store = Store(tmp_path / "outcome.sqlite")
    values = dict(event_id="industrial-event", vintage="first_release")
    values[field] = " " + values[field] + " "
    with pytest.raises(ValueError):
        store.resolve(values["event_id"], 1, ORIGIN, vintage=values["vintage"])
    assert store.db.execute("SELECT COUNT(*) FROM outcomes").fetchone()[0] == 0


@pytest.mark.parametrize("field", ("event_id", "vintage"))
def test_legacy_padded_outcome_is_reported_without_rewriting(tmp_path, field):
    store = Store(tmp_path / "legacy.sqlite")
    values = dict(event_id="industrial-event", vintage="first_release")
    values[field] = " " + values[field] + " "
    store.db.execute(
        "INSERT INTO outcomes(event_id,resolved_at,outcome,vintage) VALUES(?,?,?,?)",
        (values["event_id"], ORIGIN.isoformat(), 1, values["vintage"]),
    )
    store.db.commit()
    audit = store.audit_stored_outcomes()
    assert audit["status"] == "UNRESOLVED"
    assert audit["issues"][0]["fields"] == [field]
    assert audit["predictive_input"] is False
    row = store.db.execute("SELECT event_id,vintage FROM outcomes").fetchone()
    assert row == (values["event_id"], values["vintage"])


def test_canonical_forecast_and_outcome_stay_unscored(tmp_path):
    store = Store(tmp_path / "valid.sqlite")
    store.add_forecast(Forecast(
        "forecast-1", "industrial-event", ORIGIN, ORIGIN + timedelta(days=2),
        0.4, "diagnostic", 0.5,
    ))
    store.resolve("industrial-event", 1, ORIGIN + timedelta(days=2))
    assert store.audit_stored_outcomes()["status"] == "VALID"
    assert store.scored() == []

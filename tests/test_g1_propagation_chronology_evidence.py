"""Keep observed propagation distinct from announcements of future events.

An advance announcement may be a valid ordinary observation, but it is not
evidence that the announced propagation event has already occurred.
"""
from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations
from psychohistory.pipeline import evaluate


WHEN = datetime(2026, 10, 25, 10, tzinfo=UTC)


def observation(*, role="propagation", effective_at=WHEN, available_at=WHEN):
    return Observation(
        observation_id="industrial-event",
        series="industrial:propagation",
        effective_at=effective_at,
        available_at=available_at,
        value=1.0,
        source="first-hand",
        vintage="first",
        evidence_role=role,
        ancestry=("collector",),
        content_ancestry=("origin",),
        community_id="engineering",
    )


def test_measurement_rejects_advance_notice_as_propagation():
    row = observation(effective_at=WHEN + timedelta(days=2))
    result = validate_observations([row], WHEN + timedelta(days=3))
    assert result["valid"] is False
    assert any("propagation chronology" in error for error in result["errors"])


def test_measurement_rejects_advance_notice_across_utc_offsets():
    east = timezone(timedelta(hours=5, minutes=30))
    west = timezone(timedelta(hours=-4))
    row = observation(
        effective_at=(WHEN + timedelta(hours=1)).astimezone(east),
        available_at=WHEN.astimezone(west),
    )
    result = validate_observations([row], WHEN + timedelta(days=1))
    assert result["valid"] is False
    assert any("propagation chronology" in error for error in result["errors"])


def test_measurement_accepts_same_instant_and_delayed_reporting():
    east = timezone(timedelta(hours=5, minutes=30))
    equal = observation(available_at=WHEN.astimezone(east))
    late = replace(
        observation(available_at=WHEN + timedelta(hours=3)),
        observation_id="delayed",
    )
    result = validate_observations([equal, late], WHEN + timedelta(days=1))
    assert result["valid"] is True


def test_ordinary_advance_notice_is_not_misclassified():
    row = observation(
        role="measurement",
        effective_at=WHEN + timedelta(days=2),
    )
    assert validate_observations([row], WHEN)["valid"] is True


def test_new_store_rejects_future_propagation_event(tmp_path):
    store = Store(tmp_path / "chronology.sqlite")
    with pytest.raises(ValueError, match="propagation chronology"):
        store.add_observation(observation(effective_at=WHEN + timedelta(days=2)))


def test_store_accepts_ordinary_advance_notice(tmp_path):
    store = Store(tmp_path / "chronology.sqlite")
    store.add_observation(observation(
        role="measurement",
        effective_at=WHEN + timedelta(days=2),
    ))
    assert store.audit_stored_observations()["status"] == "VALID"


def test_legacy_audit_rejects_advance_notice_and_pipeline_fails_closed(tmp_path):
    store = Store(tmp_path / "chronology.sqlite")
    store.add_observation(observation())
    store.db.execute(
        "UPDATE observations SET effective_at=? WHERE observation_id=?",
        ((WHEN + timedelta(days=2)).isoformat(), "industrial-event"),
    )
    store.db.commit()
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert any("propagation chronology" in issue["fields"] for issue in audit["issues"])
    with pytest.raises(ValueError, match="integrity unresolved"):
        evaluate(store, WHEN + timedelta(days=3))

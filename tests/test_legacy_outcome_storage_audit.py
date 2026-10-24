"""Legacy outcome integrity is checked without rewriting historical evidence.

An outcome row is not a verified Outcome Contract or a scoring authority.
"""

from datetime import UTC, datetime, timedelta, timezone

import pytest

from psychohistory.core.store import Store
from psychohistory.pipeline import evaluate


WHEN = datetime(2026, 10, 29, 9, 30, tzinfo=UTC)


def test_empty_outcome_population_is_valid_but_not_admitted(tmp_path):
    store = Store(tmp_path / "outcomes.sqlite")
    report = store.audit_stored_outcomes()
    assert report == {
        "status": "VALID", "checked": 0, "issues": [], "predictive_input": False
    }
    assert store.scored() == []


def test_valid_first_release_and_revision_survive_audit(tmp_path):
    store = Store(tmp_path / "outcomes.sqlite")
    offset = timezone(timedelta(hours=5, minutes=30, seconds=45))
    store.resolve("industrial_event", 0, WHEN.astimezone(offset))
    store.resolve("industrial_event", 1, WHEN + timedelta(days=2), "revision_1")
    report = store.audit_stored_outcomes()
    assert report["status"] == "VALID"
    assert report["checked"] == 2
    assert report["issues"] == []
    assert store.scored() == []


@pytest.mark.parametrize(("event_id", "resolved_at", "outcome", "vintage", "field"), [
    ("bad_clock", "not-a-timestamp", 1, "first_release", "resolved_at"),
    ("naive_clock", "2026-10-29T09:30:00", 1, "first_release", "resolved_at"),
    ("missing_clock", None, 1, "first_release", "resolved_at"),
    ("missing_outcome", WHEN.isoformat(), None, "first_release", "outcome"),
    ("blank_event", WHEN.isoformat(), 1, "first_release", "event_id"),
    ("missing_event", WHEN.isoformat(), 1, "first_release", "event_id"),
    ("blank_vintage", WHEN.isoformat(), 1, " ", "vintage"),
    ("missing_vintage", WHEN.isoformat(), 1, None, "vintage"),
])
def test_legacy_outcome_corruption_is_reported(
    tmp_path, event_id, resolved_at, outcome, vintage, field
):
    if event_id == "blank_event":
        event_id = " "
    elif event_id == "missing_event":
        event_id = None
    store = Store(tmp_path / "outcomes.sqlite")
    store.db.execute(
        "INSERT INTO outcomes(event_id,resolved_at,outcome,vintage) VALUES(?,?,?,?)",
        (event_id, resolved_at, outcome, vintage),
    )
    store.db.commit()
    before = list(store.db.execute("SELECT * FROM outcomes"))
    report = store.audit_stored_outcomes()
    assert report["status"] == "UNRESOLVED"
    assert report["checked"] == 1
    assert field in report["issues"][0]["fields"]
    assert report["predictive_input"] is False
    assert list(store.db.execute("SELECT * FROM outcomes")) == before
    assert store.scored() == []


def test_pipeline_exposes_unresolved_outcome_integrity_without_scoring(tmp_path):
    store = Store(tmp_path / "outcomes.sqlite")
    store.db.execute(
        "INSERT INTO outcomes(event_id,resolved_at,outcome,vintage) VALUES(?,?,?,?)",
        ("industrial_event", "invalid", 1, "first_release"),
    )
    store.db.commit()
    report = evaluate(store, WHEN)
    assert report["outcome_integrity"]["status"] == "UNRESOLVED"
    assert report["outcome_integrity"]["predictive_input"] is False
    assert report["scoring"]["status"] == "UNMEASURED"
    assert report["claims"]["overall_brier"] == "UNMEASURED"

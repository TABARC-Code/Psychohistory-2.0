"""Read-only integrity audit for records persisted before strict insertion guards."""

from datetime import UTC, datetime, timedelta, timezone

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 24, 10, tzinfo=UTC)


def legacy_row(store, identifier, *, effective=None, available=None,
               value=1.0, quality=1.0):
    store.db.execute(
        """INSERT INTO observations
        (observation_id, series, effective_at, available_at, value, quality)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (
            identifier, "g1:meme",
            NOW.isoformat() if effective is None else effective,
            NOW.isoformat() if available is None else available,
            value, quality,
        ),
    )
    store.db.commit()


@pytest.mark.parametrize(("field", "bad"), [
    ("available", "not-a-date"),
    ("available", "2026-10-01T00:00:00"),
    ("effective", "2026-10-01T00:00:00"),
    ("effective", "0001-01-01T00:00:00+01:00"),
    ("available", "9999-12-31T23:59:59-01:00"),
])
def test_legacy_bad_clock_fails_closed_even_if_sqlite_would_hide_it(tmp_path, field, bad):
    store = Store(tmp_path / "legacy.db")
    legacy_row(store, "legacy-clock", **{field: bad})
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert audit["checked"] == 1
    assert audit["issues"] == [{
        "observation_id": "legacy-clock",
        "fields": ["effective_at" if field == "effective" else "available_at"],
    }]
    assert audit["predictive_input"] is False
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        store.observations_as_of(NOW)
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 1


@pytest.mark.parametrize(("field", "bad"), [
    ("value", b"\\x01\\x02"),
    ("quality", b"\\x01\\x02"),
    ("value", None),
    ("quality", -0.5),
])
def test_legacy_bad_measurement_cannot_reenter_evidence(tmp_path, field, bad):
    store = Store(tmp_path / "legacy.db")
    legacy_row(store, "legacy-measurement", **{field: bad})
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert audit["issues"][0]["fields"] == [field]
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        store.observations_as_of(NOW)


def test_audit_does_not_mutate_and_preserves_valid_offset_chronology(tmp_path):
    store = Store(tmp_path / "legacy.db")
    offset = timezone(timedelta(hours=5, minutes=30))
    instant = NOW.astimezone(offset)
    store.add_observation(Observation(
        "valid", "industrial_supply", instant, instant, 1.0,
        "independent-release", ancestry=("independent-1",),
    ))
    later = NOW + timedelta(microseconds=1)
    store.add_observation(Observation(
        "future", "g1:meme", later, later, 2.0, "source",
        evidence_role="propagation", content_ancestry=("root",),
    ))
    before = store.db.total_changes
    audit = store.audit_stored_observations()
    assert audit == {"status": "VALID", "checked": 2, "issues": [],
                     "predictive_input": False}
    assert store.db.total_changes == before
    assert [o.observation_id for o in store.observations_as_of(NOW)] == ["valid"]
    assert [o.observation_id for o in store.observations_as_of(later)] == [
        "valid", "future",
    ]


def test_pipeline_rejects_legacy_invalid_rows_before_g1_analysis(tmp_path):
    store = Store(tmp_path / "legacy.db")
    legacy_row(store, "unparseable", available="not-a-date")
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        evaluate(store, NOW)


def test_audit_reports_all_invalid_rows_and_fields(tmp_path):
    store = Store(tmp_path / "legacy.db")
    legacy_row(store, "bad-both", effective="bad", available="bad",
               value=b"\\x01", quality=-1)
    legacy_row(store, "bad-available", available="2026-10-01T00:00:00")
    result = store.audit_stored_observations()
    assert result["checked"] == 2
    assert result["issues"] == [
        {"observation_id": "bad-available", "fields": ["available_at"]},
        {"observation_id": "bad-both",
         "fields": ["effective_at", "available_at", "value", "quality"]},
    ]

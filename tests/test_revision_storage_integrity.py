"""Storage must enforce the same revision-metadata boundary as measurement validation."""

from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations


NOW = datetime(2026, 10, 25, 20, tzinfo=UTC)


def observation(revision_type):
    return Observation(
        observation_id="factory-output-1",
        series="industry:output",
        effective_at=NOW,
        available_at=NOW,
        value=1.0,
        source="statistics-office",
        revision_type=revision_type,
        ancestry=("release-1",),
    )


@pytest.mark.parametrize("revision_type", [None, 1, False, []])
def test_insertion_rejects_non_text_revision_before_sqlite(tmp_path, revision_type):
    store = Store(tmp_path / "revision.db")
    with pytest.raises(ValueError, match="revision"):
        store.add_observation(observation(revision_type))
    assert store.db.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 0


@pytest.mark.parametrize("revision_type", [None, 17])
def test_legacy_non_text_revision_is_audited_without_mutation(tmp_path, revision_type):
    store = Store(tmp_path / "revision.db")
    store.db.execute(
        """INSERT INTO observations
        (observation_id,series,effective_at,available_at,value,source,
         vintage,revision_type,quality)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        ("factory-output-1", "industry:output", NOW.isoformat(),
         NOW.isoformat(), 1.0, "statistics-office", "first",
         revision_type, 1.0),
    )
    store.db.commit()
    changes_before = store.db.total_changes
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert audit["checked"] == 1
    assert audit["issues"] == [{
        "observation_id": "factory-output-1", "fields": ["revision_type"]
    }]
    assert store.db.total_changes == changes_before
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        store.observations_as_of(NOW)


def test_unknown_text_revision_retains_warning_and_stores(tmp_path):
    store = Store(tmp_path / "revision.db")
    store.add_observation(observation("unclassified_release"))
    assert store.audit_stored_observations()["status"] == "VALID"
    retrieved = store.observations_as_of(NOW)
    assert len(retrieved) == 1
    result = validate_observations(retrieved, NOW)
    assert result["valid"]
    assert any("unknown revision type" in item for item in result["warnings"])

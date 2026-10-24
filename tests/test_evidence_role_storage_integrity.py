"""Persist evidence roles without silently reclassifying malformed observations."""

from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 24, 16, tzinfo=UTC)


def _observation(role):
    return Observation(
        "role-new", "g1:meme", NOW, NOW, 1.0, "independent-source",
        evidence_role=role, ancestry=("collector",),
        content_ancestry=("narrative-root",),
    )


@pytest.mark.parametrize("role", ["", " ", "unknown", 0, False, None])
def test_new_invalid_evidence_role_rejected_before_persistence(tmp_path, role):
    store = Store(tmp_path / "role.db")
    with pytest.raises(ValueError, match="evidence role"):
        store.add_observation(_observation(role))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


@pytest.mark.parametrize("role", ["", " ", "unknown", b"propagation", 0])
def test_legacy_invalid_evidence_role_fails_closed(tmp_path, role):
    store = Store(tmp_path / "legacy.db")
    store.db.execute(
        """INSERT INTO observations
        (observation_id,series,effective_at,available_at,value,quality,
         ancestry,content_ancestry,evidence_role)
        VALUES(?,?,?,?,?,?,?,?,?)""",
        ("legacy-role", "g1:meme", NOW.isoformat(), NOW.isoformat(),
         1.0, 1.0, '["collector"]', '["narrative-root"]', role),
    )
    store.db.commit()
    before = store.db.total_changes
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert audit["issues"] == [{
        "observation_id": "legacy-role", "fields": ["evidence_role"],
    }]
    assert audit["predictive_input"] is False
    assert store.db.total_changes == before
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        store.observations_as_of(NOW)
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        evaluate(store, NOW)


def test_valid_propagation_role_survives_round_trip(tmp_path):
    store = Store(tmp_path / "valid.db")
    store.add_observation(_observation("propagation"))
    assert store.audit_stored_observations()["status"] == "VALID"
    restored = store.observations_as_of(NOW)
    assert len(restored) == 1
    assert restored[0].is_propagation
    assert evaluate(store, NOW)["g1_memetics"]["propagation"]["events"] == 1


def test_legacy_sql_null_role_remains_measurement_for_compatibility(tmp_path):
    store = Store(tmp_path / "legacy-null.db")
    store.db.execute(
        """INSERT INTO observations
        (observation_id,series,effective_at,available_at,value,quality,
         ancestry,content_ancestry,evidence_role)
        VALUES(?,?,?,?,?,?,?,?,?)""",
        ("legacy-null", "historical", NOW.isoformat(), NOW.isoformat(),
         1.0, 1.0, "[]", "[]", None),
    )
    store.db.commit()
    assert store.audit_stored_observations()["status"] == "VALID"
    assert store.observations_as_of(NOW)[0].evidence_role == "measurement"

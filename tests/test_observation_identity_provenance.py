"""Observation identity and provenance must survive both entry points and storage."""

from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations
from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 24, 18, tzinfo=UTC)


def observation(**changes):
    fields = {
        "observation_id": "event-1",
        "series": "g1:meme",
        "effective_at": NOW,
        "available_at": NOW,
        "value": 1.0,
        "source": "independent-release",
        "vintage": "first",
        "evidence_role": "propagation",
        "ancestry": ("collector",),
        "content_ancestry": ("narrative-root",),
        "community_id": "community-1",
    }
    fields.update(changes)
    return Observation(**fields)


@pytest.mark.parametrize(("field", "bad"), [
    ("observation_id", None), ("observation_id", ""), ("observation_id", " "),
    ("observation_id", 0),
    ("series", None), ("series", ""), ("series", " "), ("series", 0),
    ("source", None), ("source", ""), ("source", " "),
    ("vintage", None), ("vintage", ""), ("vintage", " "),
])
def test_new_observation_refuses_missing_identity_and_provenance(tmp_path, field, bad):
    store = Store(tmp_path / "observations.db")
    with pytest.raises(ValueError, match=field):
        store.add_observation(observation(**{field: bad}))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


@pytest.mark.parametrize(("field", "bad"), [
    ("observation_id", None), ("observation_id", ""), ("observation_id", " "),
    ("series", None), ("series", ""), ("series", " "),
    ("source", ""), ("source", " "),
    ("vintage", ""), ("vintage", " "),
])
def test_legacy_malformed_identity_is_audited_and_blocks_pipeline(tmp_path, field, bad):
    store = Store(tmp_path / "legacy.db")
    fields = {
        "observation_id": "legacy-1", "series": "g1:meme",
        "effective_at": NOW.isoformat(), "available_at": NOW.isoformat(),
        "value": 1.0, "quality": 1.0, "source": "release", "vintage": "first",
    }
    fields[field] = bad
    store.db.execute(
        """INSERT INTO observations
        (observation_id,series,effective_at,available_at,value,quality,source,vintage)
        VALUES (:observation_id,:series,:effective_at,:available_at,
                :value,:quality,:source,:vintage)""",
        fields,
    )
    store.db.commit()
    before = store.db.total_changes
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert audit["checked"] == 1
    assert audit["issues"][0]["fields"] == [field]
    assert audit["predictive_input"] is False
    assert store.db.total_changes == before
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        evaluate(store, NOW)


@pytest.mark.parametrize(("field", "bad"), [
    ("observation_id", None), ("observation_id", ""), ("observation_id", []),
    ("series", ""), ("source", " "), ("vintage", ""),
])
def test_direct_validation_rejects_invalid_identity(field, bad):
    result = validate_observations([observation(**{field: bad})], NOW)
    assert result["valid"] is False
    assert any(field in error for error in result["errors"])


@pytest.mark.parametrize(("field", "bad"), [
    ("observation_id", None), ("observation_id", ""),
    ("series", ""), ("source", " "), ("vintage", ""),
])
def test_direct_g1_rejects_invalid_provenance(field, bad):
    result = analyse_memetic_observations([
        observation(**{field: bad}),
        observation(observation_id="event-2", community_id="community-2"),
    ])
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


def test_valid_identity_survives_pipeline_and_retains_lineage_bounds(tmp_path):
    store = Store(tmp_path / "valid.db")
    store.add_observation(observation())
    store.add_observation(observation(
        observation_id="event-2", community_id="community-2",
    ))
    assert store.audit_stored_observations()["status"] == "VALID"
    result = evaluate(store, NOW)
    assert result["measurement"]["valid"] is True
    assert result["g1_memetics"]["status"] == "CANDIDATE_NOT_ADMITTED"
    assert (result["g1_memetics"]["social_resonance"]
            ["cross_community_lineage_overlap_event_fraction_lower_bound"]) == 1.0
    assert result["g1_memetics"]["predictive_input"] is False


def test_legacy_null_source_and_vintage_remain_unrecorded_not_fabricated(tmp_path):
    store = Store(tmp_path / "legacy-null.db")
    store.db.execute(
        """INSERT INTO observations
        (observation_id,series,effective_at,available_at,value,quality)
        VALUES(?,?,?,?,?,?)""",
        ("legacy-1", "historical", NOW.isoformat(), NOW.isoformat(), 1.0, 1.0),
    )
    store.db.commit()
    assert store.audit_stored_observations()["status"] == "VALID"
    row = store.observations_as_of(NOW)[0]
    assert row.source is None
    assert row.vintage is None

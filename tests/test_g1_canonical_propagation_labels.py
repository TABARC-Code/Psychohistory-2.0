"""Canonical propagation labels must not invent independent communities or actors."""

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import _valid_optional_label, validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 25, 9, tzinfo=UTC)
FIELDS = ("pipeline_position", "carrier", "actor_id", "community_id", "semantic_variant")


def observation(identifier, **changes):
    fields = {
        "observation_id": identifier,
        "series": "g1:industrial",
        "effective_at": NOW,
        "available_at": NOW,
        "value": 1.0,
        "source": "measured",
        "evidence_role": "propagation",
        "ancestry": ("collector",),
        "content_ancestry": ("industrial-origin",),
        "community_id": identifier,
    }
    fields.update(changes)
    return Observation(**fields)


@pytest.mark.parametrize("bad", [" north", "north ", " north ", "\tnorth", "north\n"])
def test_shared_optional_label_validator_rejects_padded_identifiers(bad):
    assert not _valid_optional_label(bad)


@pytest.mark.parametrize("field", FIELDS)
def test_direct_g1_rejects_padded_propagation_metadata(field):
    events = [observation("a"), replace(observation("b"), **{field: " same "})]
    result = analyse_memetic_observations(events)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False
    assert "metadata" in result["reason"]


@pytest.mark.parametrize("field", FIELDS)
def test_measurement_validator_rejects_padded_propagation_metadata(field):
    events = [observation("a"), replace(observation("b"), **{field: " same "})]
    result = validate_observations(events, NOW)
    assert result["valid"] is False
    assert any(f"invalid {field}" in error for error in result["errors"])


@pytest.mark.parametrize("field", FIELDS)
def test_store_rejects_padded_propagation_metadata(tmp_path, field):
    store = Store(tmp_path / "new.db")
    with pytest.raises(ValueError, match=field):
        store.add_observation(replace(observation("a"), **{field: " same "}))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


@pytest.mark.parametrize("field", FIELDS)
def test_legacy_audit_detects_padded_propagation_metadata_without_rewriting(tmp_path, field):
    store = Store(tmp_path / "legacy.db")
    store.db.execute(
        f"""INSERT INTO observations
        (observation_id, series, effective_at, available_at, value, quality,
         ancestry, content_ancestry, evidence_role, {field})
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        ("old", "g1:industrial", NOW.isoformat(), NOW.isoformat(),
         1.0, 1.0, '["collector"]', '["industrial-origin"]',
         "propagation", " same "),
    )
    store.db.commit()
    changes = store.db.total_changes
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert audit["issues"] == [{"observation_id": "old", "fields": [field]}]
    assert store.db.total_changes == changes
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        store.observations_as_of(NOW)


def test_canonical_distinct_communities_preserve_observed_overlap(tmp_path):
    rows = [observation("a", community_id="north"),
            observation("b", community_id="south")]
    store = Store(tmp_path / "valid.db")
    for row in rows:
        store.add_observation(row)
    assert validate_observations(rows, NOW)["valid"] is True
    assert store.audit_stored_observations()["status"] == "VALID"
    result = analyse_memetic_observations(rows)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["social_resonance"][
        "cross_community_lineage_overlap_event_fraction_lower_bound"
    ] == 1.0
    assert result["predictive_input"] is False


def test_unknown_optional_labels_remain_unknown():
    assert _valid_optional_label(None)
    assert _valid_optional_label("north")

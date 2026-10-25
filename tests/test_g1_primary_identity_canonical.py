"""Canonical primary evidence identifiers across direct G1 and stored observations."""

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 25, 12, tzinfo=UTC)
FIELDS = ("observation_id", "series", "source", "vintage")


def observation(identifier="event-1"):
    return Observation(
        observation_id=identifier,
        series="g1:industrial",
        effective_at=NOW,
        available_at=NOW,
        value=1.0,
        source="first-release",
        vintage="first",
        evidence_role="propagation",
        ancestry=("collector",),
        content_ancestry=("narrative-root",),
        community_id="industrial",
    )


@pytest.mark.parametrize("field", FIELDS)
def test_direct_g1_rejects_padded_primary_evidence_identity(field):
    events = [observation(), replace(observation("event-2"), **{field: " same "})]
    result = analyse_memetic_observations(events)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False
    assert "identity" in result["reason"] or "provenance" in result["reason"]


@pytest.mark.parametrize("field", FIELDS)
def test_measurement_rejects_padded_primary_evidence_identity(field):
    row = replace(observation(), **{field: " same "})
    result = validate_observations([row], NOW)
    assert result["valid"] is False
    assert any(f"invalid {field}" in issue for issue in result["errors"])


@pytest.mark.parametrize("field", FIELDS)
def test_storage_rejects_padded_primary_evidence_identity(tmp_path, field):
    store = Store(tmp_path / "new.sqlite")
    with pytest.raises(ValueError, match=field):
        store.add_observation(replace(observation(), **{field: " same "}))
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


@pytest.mark.parametrize("field", FIELDS)
def test_historical_audit_flags_padded_primary_evidence_identity(tmp_path, field):
    store = Store(tmp_path / "historical.sqlite")
    store.add_observation(observation())
    store.db.execute(
        f"UPDATE observations SET {field}=? WHERE observation_id=?",
        (" same ", "event-1"),
    )
    store.db.commit()
    before = store.db.total_changes
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert audit["checked"] == 1
    assert field in audit["issues"][0]["fields"]
    assert store.db.total_changes == before
    with pytest.raises(ValueError, match="integrity unresolved"):
        store.observations_as_of(NOW)


def test_padded_duplicate_id_cannot_manufacture_second_event():
    rows = [observation("event-1"), observation(" event-1 ")]
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


def test_canonical_evidence_remains_measurable_and_not_admitted(tmp_path):
    rows = [
        observation("event-1"),
        replace(observation("event-2"), community_id="social"),
    ]
    store = Store(tmp_path / "valid.sqlite")
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

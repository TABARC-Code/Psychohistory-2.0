"""Canonical ancestry identifiers must not manufacture independent origins."""

from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import _valid_ancestry, validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 25, 8, tzinfo=UTC)


def observation(identifier, *, ancestry=("collector",), content=("root",)):
    return Observation(
        observation_id=identifier, series="g1:industrial",
        effective_at=NOW, available_at=NOW, value=1.0, source="source",
        evidence_role="propagation", ancestry=ancestry,
        content_ancestry=content, community_id=identifier,
    )


@pytest.mark.parametrize("value", [
    ("root ",), (" root",), (" root ",), ["root", " root"],
    ("collector\t",), ("\ncollector",),
])
def test_ancestry_validator_rejects_noncanonical_identifiers(value):
    assert not _valid_ancestry(value)


@pytest.mark.parametrize("field", ["ancestry", "content_ancestry"])
@pytest.mark.parametrize("padded", ["root ", " root", " root "])
def test_direct_g1_rejects_padded_ancestry_before_overlap(field, padded):
    first = observation("a")
    changes = {field: (padded,)}
    second = observation(
        "b", ancestry=changes.get("ancestry", ("collector",)),
        content=changes.get("content_ancestry", ("root",)),
    )
    result = analyse_memetic_observations([first, second])
    assert result["status"] == "UNRESOLVED"
    assert "ancestry" in result["reason"]
    assert result["predictive_input"] is False


@pytest.mark.parametrize("field", ["ancestry", "content_ancestry"])
def test_validation_rejects_padded_ancestry(field):
    record = observation(
        "b",
        ancestry=("collector ",) if field == "ancestry" else ("collector",),
        content=("root ",) if field == "content_ancestry" else ("root",),
    )
    result = validate_observations([observation("a"), record], NOW)
    assert result["valid"] is False
    assert any(f"invalid {('measurement' if field == 'ancestry' else 'content')} ancestry" in error
               for error in result["errors"])


@pytest.mark.parametrize("field", ["ancestry", "content_ancestry"])
def test_new_padded_ancestry_is_not_stored(tmp_path, field):
    store = Store(tmp_path / "new.db")
    record = observation(
        "a",
        ancestry=("collector ",) if field == "ancestry" else ("collector",),
        content=("root ",) if field == "content_ancestry" else ("root",),
    )
    with pytest.raises(ValueError, match="ancestry"):
        store.add_observation(record)
    assert store.db.execute("SELECT count(*) FROM observations").fetchone()[0] == 0


@pytest.mark.parametrize("field", ["ancestry", "content_ancestry"])
def test_legacy_padded_ancestry_is_audited_without_rewriting(tmp_path, field):
    store = Store(tmp_path / "legacy.db")
    store.db.execute(
        """INSERT INTO observations
        (observation_id,series,effective_at,available_at,value,quality,
         ancestry,content_ancestry)
        VALUES(?,?,?,?,?,?,?,?)""",
        ("old", "g1:industrial", NOW.isoformat(), NOW.isoformat(),
         1.0, 1.0,
         '["collector "]' if field == "ancestry" else '["collector"]',
         '["root "]' if field == "content_ancestry" else '["root"]'),
    )
    store.db.commit()
    before = store.db.total_changes
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert audit["issues"] == [{"observation_id": "old", "fields": [field]}]
    assert audit["predictive_input"] is False
    assert store.db.total_changes == before
    with pytest.raises(ValueError, match="stored observation integrity unresolved"):
        store.observations_as_of(NOW)


def test_canonical_ancestry_still_reports_genuine_cross_community_overlap():
    records = [observation("a"), observation("b")]
    result = analyse_memetic_observations(records)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    resonance = result["social_resonance"]
    assert resonance["cross_community_lineage_overlap_event_fraction_lower_bound"] == 1
    assert result["predictive_input"] is False


def test_unrecorded_ancestry_remains_valid():
    assert _valid_ancestry(())
    assert _valid_ancestry([])

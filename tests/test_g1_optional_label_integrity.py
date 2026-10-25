"""G1 propagation labels must not manufacture communities or bypass evidence checks."""

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.store import Store
from psychohistory.core.validation import validate_observations
from psychohistory.g1.memetics import analyse_memetic_observations


NOW = datetime(2026, 10, 25, tzinfo=UTC)
LABELS = ("carrier", "actor_id", "community_id", "semantic_variant", "pipeline_position")


def event(identifier="first", **labels):
    return Observation(
        observation_id=identifier,
        series="g1:narrative",
        effective_at=NOW,
        available_at=NOW,
        value=1.0,
        source="source",
        evidence_role="propagation",
        ancestry=("collector",),
        content_ancestry=("origin",),
        **labels,
    )


@pytest.mark.parametrize("field", LABELS)
@pytest.mark.parametrize("bad", ["  ", 23, True])
def test_optional_labels_fail_direct_and_general_validation(field, bad):
    rows = [event("first", community_id="a"), event("second", community_id="b")]
    rows[1] = replace(rows[1], **{field: bad})
    checked = validate_observations(rows, NOW)
    assert checked["valid"] is False
    assert any(field in error for error in checked["errors"])
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


@pytest.mark.parametrize("field", LABELS)
def test_unhashable_labels_fail_closed_instead_of_crashing(field):
    rows = [event("first", community_id="a"), event("second", community_id="b")]
    rows[1] = replace(rows[1], **{field: ["unhashable"]})
    result = analyse_memetic_observations(rows)
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False


@pytest.mark.parametrize("field", LABELS)
def test_storage_rejects_bad_optional_labels(tmp_path, field):
    store = Store(tmp_path / "labels.sqlite")
    with pytest.raises(ValueError, match=field):
        store.add_observation(event(**{field: 123}))
    assert store.db.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 0
    store.db.close()


@pytest.mark.parametrize("field", LABELS)
def test_historical_audit_catches_malformed_optional_labels(tmp_path, field):
    store = Store(tmp_path / "legacy-labels.sqlite")
    store.add_observation(event())
    store.db.execute(
        f"UPDATE observations SET {field}=? WHERE observation_id=?",
        (b"not-text", "first"),
    )
    store.db.commit()
    audit = store.audit_stored_observations()
    assert audit["status"] == "UNRESOLVED"
    assert field in audit["issues"][0]["fields"]
    with pytest.raises(ValueError, match="integrity"):
        store.observations_as_of(NOW)
    store.db.close()


def test_valid_optional_labels_and_unknowns_preserve_cross_community_bounds():
    rows = [
        event("first", community_id="a", carrier="site", semantic_variant="v1"),
        event("second", community_id="b", carrier=None, semantic_variant=None),
    ]
    assert validate_observations(rows, NOW)["valid"] is True
    result = analyse_memetic_observations(rows)
    assert result["status"] == "CANDIDATE_NOT_ADMITTED"
    bounds = result["social_resonance"]
    assert bounds["cross_community_lineage_overlap_event_fraction_lower_bound"] == 1.0
    assert bounds["cross_community_lineage_overlap_event_fraction_upper_bound"] == 1.0
    assert result["predictive_input"] is False

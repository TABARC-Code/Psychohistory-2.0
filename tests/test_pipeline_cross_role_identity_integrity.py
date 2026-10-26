"""Point-in-time G1 cannot treat colliding mixed-domain evidence as independent."""

from dataclasses import replace
from datetime import UTC, datetime

from psychohistory.core.models import Observation
from psychohistory.pipeline import evaluate


NOW = datetime(2026, 10, 26, 8, 0, tzinfo=UTC)


class VisibleStore:
    def __init__(self, observations):
        self.observations = observations

    def observations_as_of(self, as_of):
        return self.observations


def observation(identifier, role="propagation"):
    return Observation(
        observation_id=identifier,
        series="g1:narrative" if role == "propagation" else "industrial:shock",
        effective_at=NOW,
        available_at=NOW,
        value=1.0,
        source="collector",
        ancestry=("collector",),
        evidence_role=role,
        content_ancestry=("root",) if role == "propagation" else (),
        community_id="community-a" if role == "propagation" else None,
    )


def test_cross_role_duplicate_identity_blocks_pipeline_g1():
    rows = [
        observation("shared-id", "measurement"),
        observation("shared-id"),
        observation("distinct-event"),
    ]
    result = evaluate(VisibleStore(rows), NOW)
    assert not result["measurement"]["valid"]
    assert not result["g1_measurement"]["valid"]
    assert any("duplicate" in error for error in result["g1_measurement"]["errors"])
    assert result["g1_memetics"]["status"] == "UNRESOLVED"
    assert result["g1_memetics"]["predictive_input"] is False


def test_duplicate_ordinary_measurement_ids_block_mixed_g1():
    rows = [
        observation("shock", "measurement"),
        replace(observation("shock", "measurement"), series="economic:shock"),
        observation("narrative"),
    ]
    result = evaluate(VisibleStore(rows), NOW)
    assert not result["g1_measurement"]["valid"]
    assert result["g1_memetics"]["status"] == "UNRESOLVED"


def test_invalid_ordinary_identifier_cannot_be_ignored_by_pipeline():
    rows = [
        replace(observation("shock", "measurement"), observation_id=["bad", "id"]),
        observation("narrative"),
    ]
    result = evaluate(VisibleStore(rows), NOW)
    assert not result["g1_measurement"]["valid"]
    assert any("observation_id" in error for error in result["g1_measurement"]["errors"])
    assert result["g1_memetics"]["status"] == "UNRESOLVED"


def test_unrelated_ordinary_quality_failure_does_not_poison_valid_g1():
    rows = [
        replace(observation("shock", "measurement"), quality=-1.0),
        observation("narrative"),
    ]
    result = evaluate(VisibleStore(rows), NOW)
    assert not result["measurement"]["valid"]
    assert result["g1_measurement"]["valid"]
    assert result["g1_memetics"]["status"] == "CANDIDATE_NOT_ADMITTED"
    assert result["g1_memetics"]["predictive_input"] is False

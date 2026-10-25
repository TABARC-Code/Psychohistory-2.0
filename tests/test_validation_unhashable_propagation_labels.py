"""Malformed propagation labels must not crash point-in-time validation."""

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations


CUTOFF = datetime(2026, 10, 25, 20, tzinfo=UTC)


def event(identifier, **labels):
    return Observation(
        observation_id=identifier,
        series="g1:industrial-disruption",
        effective_at=CUTOFF,
        available_at=CUTOFF,
        value=1.0,
        source="independent-collector",
        evidence_role="propagation",
        ancestry=("measurement-feed",),
        content_ancestry=("reported-incident",),
        **labels,
    )


@pytest.mark.parametrize(
    "field", ("carrier", "actor_id", "community_id", "semantic_variant")
)
@pytest.mark.parametrize(
    "malformed", (["unhashable"], {"source": "unhashable"}, {"unhashable"})
)
def test_unhashable_propagation_label_is_reported_not_raised(field, malformed):
    rows = [
        event("first", carrier="site", actor_id="reporter",
              community_id="engineering", semantic_variant="v1"),
        event("second"),
    ]
    rows[1] = replace(rows[1], **{field: malformed})
    result = validate_observations(rows, CUTOFF)

    assert result["valid"] is False
    assert any(f"invalid {field}:" in error for error in result["errors"])
    assert result["propagation_event_count"] == 2
    assert result["carrier_breadth"] == 1
    assert result["actor_breadth"] == 1
    assert result["community_breadth"] == 1
    assert result["semantic_variant_breadth"] == 1


def test_unhashable_pipeline_position_is_invalid_without_crashing():
    result = validate_observations(
        [event("first", pipeline_position=["unhashable"])], CUTOFF
    )
    assert result["valid"] is False
    assert any("invalid pipeline_position:" in error for error in result["errors"])


def test_valid_labels_still_count_distinct_communities():
    result = validate_observations(
        [event("first", community_id="engineering", carrier="site"),
         event("second", community_id="public", carrier="site")],
        CUTOFF,
    )
    assert result["valid"] is True
    assert result["community_breadth"] == 2
    assert result["carrier_breadth"] == 1

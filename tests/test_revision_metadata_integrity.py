"""Revision metadata must not crash point-in-time measurement validation."""

from datetime import UTC, datetime

import pytest

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations


NOW = datetime(2026, 10, 25, 12, tzinfo=UTC)


def _observation(revision_type):
    return Observation(
        observation_id="industrial-shock-1",
        series="industrial:output",
        effective_at=NOW,
        available_at=NOW,
        value=1.0,
        source="published-statistics",
        revision_type=revision_type,
        ancestry=("statistics-office",),
    )


@pytest.mark.parametrize("revision_type", [[], {}, None])
def test_non_text_revision_metadata_is_invalid_without_crashing(revision_type):
    result = validate_observations([_observation(revision_type)], NOW)
    assert result["valid"] is False
    assert any("invalid revision type" in error for error in result["errors"])


def test_unknown_text_revision_type_retains_legacy_warning():
    result = validate_observations([_observation("unclassified_release")], NOW)
    assert result["valid"] is True
    assert any("unknown revision type" in warning for warning in result["warnings"])


def test_known_revision_type_remains_valid():
    result = validate_observations([_observation("scheduled_revision")], NOW)
    assert result["valid"] is True
    assert not result["warnings"]

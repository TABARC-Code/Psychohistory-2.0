from datetime import UTC, datetime

from psychohistory.core.models import Observation
from psychohistory.core.validation import validate_observations


WHEN = datetime(2026, 10, 17, tzinfo=UTC)


def row(identifier, role, ancestry=(), content_ancestry=()):
    return Observation(
        identifier, "narrative" if role == "propagation" else "energy",
        WHEN, WHEN, 1.0, "collector", evidence_role=role,
        ancestry=ancestry, content_ancestry=content_ancestry,
    )


def test_shared_collector_between_shock_and_meme_is_visible():
    result = validate_observations([
        row("shock", "measurement", ("collector-1",)),
        row("meme", "propagation", ("collector-1",), ("meme-root",)),
    ], WHEN)
    assert result["shared_cross_role_measurement_ancestry"] == {
        "collector-1": {"measurement_events": 1, "propagation_events": 1}
    }
    assert result["cross_role_measurement_ancestry_status"] == "OBSERVED_SHARED"
    assert result["shared_content_ancestry"] == {}
    assert result["content_ancestry_coverage_fraction"] == 1.0


def test_cross_role_counts_deduplicate_repeated_tokens_per_event():
    result = validate_observations([
        row("shock", "measurement", ("same", "same")),
        row("meme", "propagation", ("same", "same")),
        row("meme2", "propagation", ("same",), ("root",)),
    ], WHEN)
    assert result["shared_cross_role_measurement_ancestry"]["same"] == {
        "measurement_events": 1, "propagation_events": 2
    }


def test_no_common_ancestor_with_full_coverage_is_observed_absence_only():
    result = validate_observations([
        row("shock", "measurement", ("shock-root",)),
        row("meme", "propagation", ("collector-root",), ("meme-root",)),
    ], WHEN)
    assert result["shared_cross_role_measurement_ancestry"] == {}
    assert result["cross_role_measurement_ancestry_status"] == "NO_SHARED_OBSERVED"
    assert result["measurement_ancestry_coverage_fraction"] == 1.0
    assert result["propagation_measurement_ancestry_coverage_fraction"] == 1.0


def test_missing_ancestry_does_not_claim_independence():
    result = validate_observations([
        row("shock", "measurement"),
        row("meme", "propagation", ("collector-root",)),
    ], WHEN)
    assert result["shared_cross_role_measurement_ancestry"] == {}
    assert result["cross_role_measurement_ancestry_status"] == "PARTIAL_UNMEASURED"
    assert result["measurement_ancestry_coverage_fraction"] == 0.0
    assert result["propagation_measurement_ancestry_coverage_fraction"] == 1.0

"""Cross-domain lag sidecar: chronological order is not predictive admission."""
from datetime import UTC, datetime, timedelta

import pytest

from psychohistory.core.bidirectional import DirectedHypothesis
from psychohistory.core.models import Observation
from psychohistory.sidecars.lag_audit import audit_directional_lags


START = datetime(2026, 10, 1, tzinfo=UTC)
CUTOFF = START + timedelta(days=6)


def row(identifier, series, days, *, available_days=None, ancestry=("collector",),
        content_ancestry=(), propagation=False):
    effective = START + timedelta(days=days)
    available = effective if available_days is None else START + timedelta(days=available_days)
    return Observation(
        identifier, series, effective, available, 1.0, "publisher",
        ancestry=ancestry, content_ancestry=content_ancestry,
        evidence_role="propagation" if propagation else "measurement",
    )


def test_reciprocal_lags_keep_direction_and_shared_measurement_source_separate():
    observations = [
        row("narrative", "g1", 0, propagation=True),
        row("industrial", "industry", 2.25),
    ]
    hypotheses = [
        DirectedHypothesis("g1", "industry", 2, 0.3, True, ("source-1",)),
        DirectedHypothesis("industry", "g1", 2),
    ]
    result = audit_directional_lags(observations, CUTOFF, hypotheses)
    forward, reverse = result["directional_lags"]
    assert forward["observed_pair_count"] == 1
    assert forward["source_available_before_target_count"] == 1
    assert forward["shared_measurement_ancestry_pair_count"] == 1
    assert reverse["observed_pair_count"] == 0
    assert result["reciprocal_registry"][0]["reverse_present"] is True
    assert result["reciprocal_registry"][0]["admission_claimed_unverified"] is True
    assert result["reciprocal_registry"][0]["admitted"] is False
    assert result["forecast_admission_status"] == "CLOSED"
    assert result["predictive_input"] is False


def test_retrospectively_available_narrative_is_not_counted_as_early_warning():
    observations = [
        row("narrative", "g1", 0, available_days=3, propagation=True),
        row("industrial", "industry", 2),
    ]
    result = audit_directional_lags(
        observations, CUTOFF, [DirectedHypothesis("g1", "industry", 2)]
    )
    item = result["directional_lags"][0]
    assert item["observed_pair_count"] == 1
    assert item["source_available_before_target_count"] == 0
    assert item["retrospective_or_contemporaneous_pair_count"] == 1


def test_same_instant_cannot_be_claimed_as_a_lead():
    observations = [
        row("g1", "g1", 1, propagation=True),
        row("social", "social", 1),
    ]
    item = audit_directional_lags(
        observations, CUTOFF, [DirectedHypothesis("g1", "social", 0)]
    )["directional_lags"][0]
    assert item["observed_pair_count"] == 1
    assert item["source_available_before_target_count"] == 0


def test_missing_measurement_ancestry_does_not_claim_independence():
    observations = [
        row("g1", "g1", 0, ancestry=(), propagation=True),
        row("security", "security", 1, ancestry=("collector",)),
    ]
    item = audit_directional_lags(
        observations, CUTOFF, [DirectedHypothesis("g1", "security", 1)]
    )["directional_lags"][0]
    assert item["unknown_measurement_ancestry_pair_count"] == 1
    assert item["independence_status"] == "UNVERIFIED"


def test_future_available_observations_fail_closed():
    observations = [
        row("g1", "g1", 0, available_days=7, propagation=True),
        row("health", "health", 2),
    ]
    result = audit_directional_lags(
        observations, CUTOFF, [DirectedHypothesis("g1", "health", 2)]
    )
    assert result["status"] == "UNRESOLVED"
    assert result["predictive_input"] is False
    assert "directional_lags" not in result


def test_future_effective_propagation_is_excluded_even_if_announced():
    observations = [
        row("scheduled", "g1", 8, available_days=1, propagation=True),
        row("economic", "economy", 2),
    ]
    result = audit_directional_lags(
        observations, CUTOFF, [DirectedHypothesis("g1", "economy", 0)]
    )
    assert result["status"] == "DIAGNOSTIC_ONLY"
    assert result["excluded_future_effective_observations"] == 1
    assert result["directional_lags"][0]["observed_pair_count"] == 0


def test_duplicate_hypothesis_is_rejected_before_pair_counts():
    with pytest.raises(ValueError, match="duplicate"):
        audit_directional_lags(
            [], CUTOFF,
            [DirectedHypothesis("g1", "g2", 1), DirectedHypothesis("g1", "g2", 1)],
        )


def test_elapsed_days_are_not_calendar_dates_or_rounded_hours():
    observations = [
        row("g1", "g1", 0.9, propagation=True),
        row("health", "health", 1.1),
    ]
    result = audit_directional_lags(
        observations, CUTOFF, [DirectedHypothesis("g1", "health", 0)]
    )
    assert result["directional_lags"][0]["observed_pair_count"] == 1


def test_preannounced_consequence_is_not_an_independent_narrative_lead():
    observations = [
        row("narrative", "g1", 1, propagation=True),
        row("announced-shock", "industry", 2, available_days=0),
    ]
    item = audit_directional_lags(
        observations, CUTOFF, [DirectedHypothesis("g1", "industry", 1)]
    )["directional_lags"][0]
    assert item["observed_pair_count"] == 1
    assert item["source_available_before_target_count"] == 1
    assert item["target_preannounced_pair_count"] == 1
    assert item["source_available_before_target_first_release_count"] == 0

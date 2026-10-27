"""Point-in-time directional lag audit for cross-domain observation series.

This sidecar counts observed event orderings. It is not a Hawkes fit, causal
estimator, exposure adjustment, independent evidence test or forecast gate.
An observed ordering must not be promoted to predictive admission.
"""

from collections import defaultdict
from datetime import UTC

from ..core.bidirectional import DirectedHypothesis, reciprocal_view
from ..core.validation import _aware_instant, validate_observations


def audit_directional_lags(observations, as_of, hypotheses):
    """Count exact elapsed-day lag bins without inferring transmission.

    A lag of d days means a nonnegative physical-time separation in
    [d, d+1) elapsed days, not a calendar-date difference. Count a
    chronologically available source separately from retrospective pairs.
    The target's outcome contract, source exposure and common shocks are
    not verified here.
    """
    if not _aware_instant(as_of):
        raise ValueError("as_of must be a UTC-convertible aware datetime")
    rows = list(observations)
    hypotheses = list(hypotheses)
    if any(type(h) is not DirectedHypothesis for h in hypotheses):
        raise ValueError("hypotheses must be DirectedHypothesis instances")
    # This rejects duplicate directional/lag hypotheses before reporting
    # any family size or pair count. Caller-supplied admission is ignored.
    registry = reciprocal_view(hypotheses)
    checked = validate_observations(rows, as_of)
    if not checked["valid"]:
        return {
            "status": "UNRESOLVED",
            "reason": "point-in-time observation validation failed",
            "measurement_errors": checked["errors"],
            "predictive_input": False,
        }

    cutoff = as_of.astimezone(UTC)
    by_series = defaultdict(list)
    excluded_future_effective = 0
    for row in rows:
        effective = row.effective_at.astimezone(UTC)
        if effective > cutoff:
            excluded_future_effective += 1
        else:
            by_series[row.series].append((
                row, effective, row.available_at.astimezone(UTC)
            ))

    diagnostics = []
    for hypothesis in hypotheses:
        counts = {
            "observed_pair_count": 0,
            "source_available_before_target_count": 0,
            "source_available_before_target_first_release_count": 0,
            "source_available_before_target_and_first_release_count": 0,
            "target_preannounced_pair_count": 0,
            "retrospective_or_contemporaneous_pair_count": 0,
            "shared_measurement_ancestry_pair_count": 0,
            "unknown_measurement_ancestry_pair_count": 0,
            "shared_content_ancestry_pair_count": 0,
        }
        for source, source_time, source_available in by_series[hypothesis.source]:
            for target, target_time, target_available in by_series[hypothesis.target]:
                lag = target_time - source_time
                if lag.days != hypothesis.lag_days or lag.days < 0:
                    continue
                counts["observed_pair_count"] += 1
                if target_available < target_time:
                    counts["target_preannounced_pair_count"] += 1
                if source_time < target_time and source_available < target_available:
                    counts["source_available_before_target_first_release_count"] += 1
                # Marginal lead and preannouncement counts do not reveal
                # whether the *same pair* preceded both the physical event
                # and its first release. Preserve that intersection directly.
                if (source_time < target_time
                        and source_available < target_time
                        and source_available < target_available):
                    counts["source_available_before_target_and_first_release_count"] += 1
                # Availability strictly before the consequence is necessary
                # for a leading observation, but is not sufficient for skill.
                if source_time < target_time and source_available < target_time:
                    counts["source_available_before_target_count"] += 1
                else:
                    counts["retrospective_or_contemporaneous_pair_count"] += 1
                if not source.ancestry or not target.ancestry:
                    counts["unknown_measurement_ancestry_pair_count"] += 1
                elif set(source.ancestry) & set(target.ancestry):
                    counts["shared_measurement_ancestry_pair_count"] += 1
                if (source.is_propagation and target.is_propagation
                        and set(source.content_ancestry) & set(target.content_ancestry)):
                    counts["shared_content_ancestry_pair_count"] += 1
        diagnostics.append({
            "source": hypothesis.source,
            "target": hypothesis.target,
            "lag_days": hypothesis.lag_days,
            **counts,
            "independence_status": "UNVERIFIED",
            "exposure_status": "UNMEASURED",
            "common_shock_status": "UNVERIFIED",
            "predictive_input": False,
        })
    return {
        "status": "DIAGNOSTIC_ONLY" if hypotheses else "UNMEASURED",
        "as_of": as_of.isoformat(),
        "excluded_future_effective_observations": excluded_future_effective,
        "directional_lags": diagnostics,
        "reciprocal_registry": registry,
        "measurement_status": "VALID",
        "network_inference_status": "UNVERIFIED",
        "multiplicity_status": "UNVERIFIED",
        "forecast_admission_status": "CLOSED",
        "predictive_input": False,
    }

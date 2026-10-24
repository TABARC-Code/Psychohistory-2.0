from datetime import UTC

from .core.validation import _aware_instant, validate_observations
from .g1.memetics import analyse_memetic_observations
from .validation.scoring import brier


def _effective_by(observation, cutoff):
    effective = observation.effective_at
    return _aware_instant(effective) and effective.astimezone(UTC) <= cutoff


def evaluate(store, as_of):
    if not _aware_instant(as_of):
        raise ValueError("as_of must be a timezone-aware datetime")
    cutoff = as_of.astimezone(UTC)
    obs = store.observations_as_of(as_of)
    # Store.scored() has no historical cutoff, registration check or outcome
    # contract verification. Keep retrospective scoring unmeasured.
    scored = []
    measurement = validate_observations(obs, as_of)
    g1_candidates = [o for o in obs if o.is_propagation]
    # Availability establishes what was knowable; effective_at establishes
    # whether the propagation event itself had occurred by this cutoff.
    g1_obs = [o for o in g1_candidates if _effective_by(o, cutoff)]
    # Check all candidates before event-time filtering: invalid clocks must
    # not disappear and make the remaining G1 sample appear valid. Keep
    # measurement summaries limited to events effective at this cutoff.
    candidate_validation = validate_observations(g1_candidates, as_of)
    g1_measurement = (
        validate_observations(g1_obs, as_of)
        if candidate_validation["valid"] else candidate_validation
    )
    if g1_measurement["valid"]:
        memetics = analyse_memetic_observations(g1_obs)
    else:
        memetics = {
            "status": "UNRESOLVED",
            "reason": "observation measurement validation failed",
            "predictive_input": False,
        }
    return {
        "as_of": as_of.isoformat(),
        "measurement": measurement,
        "g1_measurement": g1_measurement,
        "n_observations": len(obs),
        "g1_memetics": memetics,
        "g1_excluded_future_or_unverifiable_effective_at": (
            len(g1_candidates) - len(g1_obs)
        ),
        "scoring": {
            **brier(scored),
            "reason": "registration and Outcome Contract verification unavailable",
        },
        "claims": {
            "overall_brier": "MEASURED" if scored else "UNMEASURED",
            "calibration": "UNMEASURED",
            "false_alert_rate": "UNMEASURED",
            "lead_time_advantage": "UNMEASURED",
        },
    }

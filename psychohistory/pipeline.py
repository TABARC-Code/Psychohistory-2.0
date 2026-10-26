from datetime import UTC

from .core.validation import _aware_instant, _valid_primary_label, validate_observations
from .g1.memetics import analyse_memetic_observations
from .validation.scoring import brier


def _effective_by(observation, cutoff):
    effective = observation.effective_at
    return _aware_instant(effective) and effective.astimezone(UTC) <= cutoff



def _sample_identity_errors(observations):
    """A mixed point-in-time sample shares one observation ID namespace."""
    seen = set()
    errors = []
    for row in observations:
        identifier = row.observation_id
        if not _valid_primary_label(identifier):
            errors.append(f"invalid observation_id: {identifier!r}")
        elif identifier in seen:
            errors.append(f"duplicate id: {identifier}")
        else:
            seen.add(identifier)
    return errors


def evaluate(store, as_of):
    if not _aware_instant(as_of):
        raise ValueError("as_of must be a timezone-aware datetime")
    cutoff = as_of.astimezone(UTC)
    obs = store.observations_as_of(as_of)
    # Store.scored() has no historical cutoff, registration check or outcome
    # contract verification. Keep retrospective scoring unmeasured.
    scored = []
    # Historical outcome rows are diagnostic evidence until independently
    # matched to immutable registrations and outcome contracts.
    outcome_audit = getattr(store, "audit_stored_outcomes", None)
    outcome_integrity = (
        outcome_audit() if callable(outcome_audit) else {
            "status": "UNVERIFIED", "checked": 0, "issues": [],
            "predictive_input": False,
        }
    )
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
    # The G1 subset must not silently discard an identity collision in the
    # surrounding industrial, economic or other measurement evidence.
    # Keep unrelated measurement quality failures local to their own domain.
    identity_errors = _sample_identity_errors(obs)
    if identity_errors:
        g1_measurement = {
            **g1_measurement,
            "valid": False,
            "errors": list(dict.fromkeys([
                *g1_measurement["errors"], *identity_errors,
            ])),
        }
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
        "outcome_integrity": outcome_integrity,
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

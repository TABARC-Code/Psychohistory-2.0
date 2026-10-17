from .core.validation import validate_observations
from .g1.memetics import analyse_memetic_observations
from .validation.scoring import brier


def evaluate(store, as_of):
    obs = store.observations_as_of(as_of)
    # Store.scored() has no historical cutoff, registration check or outcome
    # contract verification. Keep retrospective scoring unmeasured.
    scored = []
    measurement = validate_observations(obs, as_of)
    g1_obs = [o for o in obs if o.is_propagation]
    g1_measurement = validate_observations(g1_obs, as_of)
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

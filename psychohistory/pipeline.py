from .core.validation import validate_observations
from .g1.memetics import analyse_memetic_observations
from .validation.scoring import brier


def evaluate(store, as_of):
    obs = store.observations_as_of(as_of)
    scored = store.scored()
    return {
        "as_of": as_of.isoformat(),
        "measurement": validate_observations(obs, as_of),
        "n_observations": len(obs),
        "g1_memetics": analyse_memetic_observations(obs),
        "scoring": brier(scored),
        "claims": {
            "overall_brier": "MEASURED" if scored else "UNMEASURED",
            "calibration": "UNMEASURED",
            "false_alert_rate": "UNMEASURED",
            "lead_time_advantage": "UNMEASURED",
        },
    }

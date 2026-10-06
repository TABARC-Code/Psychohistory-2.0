from .core.validation import validate_observations
from .validation.scoring import brier

def evaluate(store,as_of):
    obs=store.observations_as_of(as_of)
    return {'as_of':as_of.isoformat(),'measurement':validate_observations(obs,as_of),'n_observations':len(obs),'scoring':brier(store.scored()),'claims':{'overall_brier':'MEASURED' if store.scored() else 'UNMEASURED','calibration':'UNMEASURED','false_alert_rate':'UNMEASURED','lead_time_advantage':'UNMEASURED'}}
